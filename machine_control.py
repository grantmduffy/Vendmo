from transactions import get_incomplete
from servo import dispense_beer
from time import sleep
from settings import Settings

run = True
refresh_rate = 5
s = Settings()


def controller_daemon():
    while run:
        incomplete_transactions = get_incomplete()
        if not incomplete_transactions.empty:
            for i, transaction in incomplete_transactions.iterrows():
                actor, amount, completed = transaction
                if amount >= s.price:
                    # TODO: Drive LCD
                    print(f'This beer is for {actor}')
                    dispense_beer()
        sleep(refresh_rate)


if __name__ == '__main__':
    controller_daemon()