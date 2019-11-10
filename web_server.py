from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from subprocess import Popen
from sys import platform
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh! this is secret!'
Bootstrap(app)

if platform == 'linux':
    files_folder = '/home/pi/'
    password_file = files_folder + 'password.txt'
else:
    password_file = 'password.txt'


def get_password():
    try:
        with open(password_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        with open(password_file, 'w') as f:
            f.write(generate_password_hash('Vendmo', method='sha256'))
        return get_password()


def set_password(hashed_password):
    with open('password.txt', 'w') as f:
        f.write(hashed_password)


class LoginForm(FlaskForm):
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])


class SettingsForm(FlaskForm):
    old_password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    new_password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if check_password_hash(get_password(), form.password.data):
            return redirect(url_for('settings'))
        else:
            return '<h2>Invalid Password</h2><a href="/login">return</a>'
    return render_template('login.html', form=form)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    login_form = LoginForm()
    settings_form = SettingsForm()

    if login_form.validate_on_submit():
        print('Entered')
        if check_password_hash(get_password(), login_form.password.data):
            return render_template('settings.html', form=settings_form)

    if settings_form.validate_on_submit():
        if check_password_hash(get_password(), settings_form.old_password.data):
            set_password(generate_password_hash(settings_form.new_password.data, method='sha256'))
            return render_template('settings.html', form=settings_form)

    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
