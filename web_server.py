from flask import Flask, render_template, request
from flask_basicauth import BasicAuth
from flask_bootstrap import Bootstrap
from settings import Settings
from transactions import get_html
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Form
from time import sleep
from sys import platform
import os

app = Flask(__name__)
Bootstrap(app)

s = Settings()

app.config['SECRET_KEY'] = 'shhh! this is secret!'
app.config['BASIC_AUTH_USERNAME'] = s.username
app.config['BASIC_AUTH_PASSWORD'] = s.password
auth = BasicAuth(app)

wifi_config_loc = '/boot/wpa_supplicant.conf'


class UserForm(FlaskForm):
    username = StringField('New Username')
    password = PasswordField('New Password')
    submit = SubmitField('Update')


class EmailForm(FlaskForm):
    address = StringField('Email Address')
    password = PasswordField('Password')
    submit = SubmitField('Update')


class WifiForm(FlaskForm):
    ssid = StringField('Wifi SSID')
    password = PasswordField('Password')
    submit = SubmitField('Update')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/settings', methods=['GET'])
@auth.required
def settings():
    print('In /settings')
    user_form = UserForm()
    email_form = EmailForm()
    wifi_form = WifiForm()
    return render_template('settings.html', user_form=user_form, email_form=email_form, wifi_form=wifi_form)


@app.route('/update_login', methods=['POST'])
@auth.required
def update_login():
    user_form = UserForm()
    email_form = EmailForm()
    wifi_form = WifiForm()
    if user_form.validate_on_submit():
        s.username = user_form.username.data
        s.password = user_form.password.data
        app.config['BASIC_AUTH_USERNAME'] = s.username
        app.config['BASIC_AUTH_PASSWORD'] = s.password
        print('Login Updated')
    return render_template('settings.html', user_form=user_form, email_form=email_form, wifi_form=wifi_form)


@app.route('/update_email', methods=['POST'])
@auth.required
def update_email():
    user_form = UserForm()
    email_form = EmailForm()
    wifi_form = WifiForm()
    if email_form.validate_on_submit():
        s.email_address = email_form.address.data
        s.email_password = email_form.password.data
        print('Email Updated')
    return render_template('settings.html', user_form=user_form, email_form=email_form, wifi_form=wifi_form)


@app.route('/update_wifi', methods=['POST'])
@auth.required
def update_wifi():
    user_form = UserForm()
    email_form = EmailForm()
    wifi_form = WifiForm()
    if wifi_form.validate_on_submit():
        ssid = wifi_form.ssid.data
        password = wifi_form.password.data
        if platform == 'linux':
            with open(wifi_config_loc, 'w') as f:
                f.write(
                    'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n'
                    'update_config=1\n'
                    'country=US\n'
                    'network={\n'
                    f'   ssid="{ssid}"\n'
                    f'   psk="{password}"\n'
                    '   key_mgmt=WPA-PSK\n'
                    '}\n'
                )
            sleep(3)
            os.system('sudo reboot')
        print('WiFi Updated')
    return render_template('settings.html', user_form=user_form, email_form=email_form, wifi_form=wifi_form)


@app.route('/transactions')
def transactions():
    return render_template('transactions.html', table=get_html())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
