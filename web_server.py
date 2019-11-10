from flask import Flask, render_template
from subprocess import Popen
from sys import platform

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('web_interface.html')


@app.route('/reboot')
def reboot():
    if platform == 'linux':
        Popen('sleep 5s;sudo reboot', shell=True)
        # TODO: do cleanup
        exit()
    else:
        print('Reboot Raspberry Pi...')
    return '<h1>Rebooting Raspberry Pi...</h1>' \
           '<a href="/">home</a>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
