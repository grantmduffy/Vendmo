from flask import Flask, render_template, request
from flask_basicauth import BasicAuth
from flask_bootstrap import Bootstrap
from settings import Settings
from transactions import get_html
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from time import sleep
from sys import platform
from servo import dispense_beer
from threading import Thread
import json
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


class VenmoForm(FlaskForm):
    venmo_user = StringField('Venmo User ID')
    price = FloatField('Set Price')
    phrase = StringField('Set Phrase')
    submit = SubmitField('Update')


def restart_pi(delay=3):
    def helper():
        sleep(delay)
        os.system('sudo reboot')
    if platform == 'linux':
        Thread(target=helper).start()
    else:
        print('Restarting...')


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
    venmo_form = VenmoForm()
    return render_template('settings.html', user_form=user_form, email_form=email_form,
                           wifi_form=wifi_form, venmo_form=venmo_form)


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
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/update_email', methods=['POST'])
@auth.required
def update_email():
    email_form = EmailForm()
    if email_form.validate_on_submit():
        s.email_address = email_form.address.data
        s.email_password = email_form.password.data
        print('Email Updated')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/update_wifi', methods=['POST'])
@auth.required
def update_wifi():
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
            restart_pi()
        print('WiFi Updated')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/update_venmo', methods=['POST'])
@auth.required
def update_venmo():
    venmo_form = VenmoForm()
    if venmo_form.validate_on_submit():
        venmo_user = venmo_form.venmo_user.data
        price = venmo_form.price.data
        phrase = venmo_form.phrase.data
        s.price = price
        s.user_phrase = phrase
        s.venmo_user = venmo_user
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/transactions')
def transactions():
    return render_template('transactions.html', table=get_html())


@app.route('/dispense', methods=['POST'])
@auth.required
def dispense():
    dispense_beer()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/restart', methods=['POST'])
@auth.required
def restart():
    restart_pi()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
