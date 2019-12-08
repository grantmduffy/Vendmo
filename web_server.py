from flask import Flask, render_template
from flask_basicauth import BasicAuth
from flask_bootstrap import Bootstrap
from settings import Settings
from transactions import get_html
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

app = Flask(__name__)
Bootstrap(app)

s = Settings()

app.config['SECRET_KEY'] = 'shhh! this is secret!'
app.config['BASIC_AUTH_USERNAME'] = s.username
app.config['BASIC_AUTH_PASSWORD'] = s.password

auth = BasicAuth(app)


class UserForm(FlaskForm):
    username = StringField('New Username')
    password = PasswordField('New Password')


class EmailForm(FlaskForm):
    address = StringField('Email Address')
    password = PasswordField('Password')


class WifiForm(FlaskForm):
    ssid = StringField('Wifi SSID')
    password = PasswordField('Password')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/settings', methods=['GET', 'POST'])
@auth.required
def settings():
    user_form = UserForm()
    email_form = EmailForm()
    wifi_form = WifiForm()

    if user_form.validate():
        s.username = user_form.username.data
        s.password = user_form.password.data
        app.config['BASIC_AUTH_USERNAME'] = s.username
        app.config['BASIC_AUTH_PASSWORD'] = s.password

    if email_form.validate():
        s.email_address = email_form.address.data
        s.email_password = email_form.password.data

    if wifi_form.validate():
        ssid = wifi_form.ssid.data
        password = wifi_form.password.data
        print(ssid, password)

    return render_template('settings.html', user_form=user_form, email_form=email_form, wifi_form=wifi_form)


@app.route('/transactions')
def transactions():
    return render_template('transactions.html', table=get_html())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
