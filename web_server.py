from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from subprocess import Popen
from sys import platform
from werkzeug.security import generate_password_hash, check_password_hash
from json import dumps, loads
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh! this is secret!'
Bootstrap(app)


class Settings:

    defaults = {
        'password': generate_password_hash('Vendmo', method='sha256'),
        'email_address': '',
        'email_password': ''
    }
    file = 'settings.json'

    def __init__(self):
        if platform == 'linux':
            self.file = '/home/pi/' + self.file

    def _load(self):
        try:
            with open(self.file, 'r') as f:
                return loads(f.read())
        except FileNotFoundError:
            with open(self.file, 'w') as f:
                f.write(dumps(self.defaults))
            return self._load()

    def __getattr__(self, item):
        return self._load()[item]

    def __setattr__(self, key, value):
        s = self._load()
        s[key] = value
        with open(self.file, 'w') as f:
            f.write(dumps(s))


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[Length(min=0, max=80)])


class SettingsForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[Length(min=0, max=80)])
    new_password = PasswordField('New Password', validators=[Length(min=0, max=80)])
    email_address = StringField('Email Address', validators=[Email()])
    email_password = PasswordField('Email Password', validators=[Length(min=0, max=80)])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/reboot')
def reboot():
    if platform == 'linux':
        Popen('sleep 3s;sudo reboot', shell=True)
        # TODO: do cleanup
    else:
        print('Reboot Raspberry Pi...')
    return '<h1>Rebooting Raspberry Pi...</h1>' \
           '<a href="/">home</a>'


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    s = Settings()
    login_form = LoginForm()
    settings_form = SettingsForm()

    if login_form.validate_on_submit():
        if login_form.password.data and check_password_hash(s.password, login_form.password.data):
            return render_template('settings.html', form=settings_form)

    if settings_form.validate_on_submit():
        if settings_form.old_password.data and settings_form.new_password.data and\
                check_password_hash(s.password, settings_form.old_password.data):
            s.password = generate_password_hash(settings_form.new_password.data, method='sha256')
        return render_template('settings.html', form=settings_form)

    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
