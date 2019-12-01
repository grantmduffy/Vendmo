from threading import Thread
from machine_email import receipt_daemon
from machine_control import controller_daemon
from web_server import app

machine_control_thread = Thread(target=controller_daemon)
email_thread = Thread(target=receipt_daemon)


if __name__ == '__main__':
    machine_control_thread.start()
    email_thread.start()
    app.run(debug=True, host='0.0.0.0')
