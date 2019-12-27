from threading import Thread
from machine_email import check_venmos
from web_server import app
from transactions import add_transaction
from servo import dispense_beer
from time import sleep
from settings import Settings

run = True
refresh_rate = 5
s = Settings()


def worker():
    while run:
        venmos = check_venmos()
        for venmo in venmos:
            if venmo['Amount'] >= s.price:
                dispense_beer()
                # TODO: Drive LCD
            add_transaction(venmo)
        sleep(refresh_rate)


if __name__ == '__main__':
    t = Thread(target=worker)
    t.start()
    app.run(debug=True, host='0.0.0.0')
