from threading import Thread
from machine_email import check_venmos
from web_server import app
from transactions import add_transactions, get_incomplete
from servo import dispense_beer
from time import sleep
from settings import Settings

run = True
refresh_rate = 5
s = Settings()


def worker():
    while run:
        venmos = check_venmos()
        if venmos:
            add_transactions(venmos)
        for t in get_incomplete():
            # TODO: Drive LCD
            if t['Amount'] >= s.price:
                print(f'This beer is for {t["Actor"]}')
                dispense_beer()
        sleep(refresh_rate)


if __name__ == '__main__':
    t = Thread(target=worker)
    t.start()
    app.run(debug=True, host='0.0.0.0')
