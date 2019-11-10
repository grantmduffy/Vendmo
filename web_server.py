from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from subprocess import Popen
from sys import platform
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh! this is secret!'
Bootstrap(app)

if platform == 'linux':
    files_folder = '/home/pi/'
else:
    files_folder = ''
password_file = files_folder + 'password.txt'


def get_password():
    try:
        with open(password_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        with open(password_file, 'w') as f:
            f.write(generate_password_hash('Vendmo', method='sha256'))
        return get_password()


def set_password(hashed_password):
    with open(password_file, 'w') as f:
        f.write(hashed_password)


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
    login_form = LoginForm()
    settings_form = SettingsForm()

    if login_form.validate_on_submit():
        if login_form.password.data and check_password_hash(get_password(), login_form.password.data):
            return render_template('settings.html', form=settings_form)

    if settings_form.validate_on_submit():
        if settings_form.old_password.data and settings_form.new_password.data and\
                check_password_hash(get_password(), settings_form.old_password.data):
            set_password(generate_password_hash(settings_form.new_password.data, method='sha256'))
        return render_template('settings.html', form=settings_form)

    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
