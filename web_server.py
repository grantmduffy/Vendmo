from flask import Flask, render_template
import subprocess
from sys import platform

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('web_interface.html')


@app.route('/reboot')
def reboot():
    if platform == 'linux':
        # TODO: Schedule reboot and do cleanup
        subprocess.call('reboot')
    else:
        print('Reboot Raspberry Pi...')
    return '<h1>Rebooting Raspberry Pi...</h1>' \
           '<a href="/">home</a>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
