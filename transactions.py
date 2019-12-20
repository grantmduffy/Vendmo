from threading import Lock
from sys import platform
import pickle
import pandas as pd
import json

lock = Lock()

file = 'transactions.json'
# if platform == 'linux':
#     file = '/home/pi/' + file


def get_transactions():
    try:
        with lock:
            with open(file, 'r') as f:
                return json.load(f)
    except FileNotFoundError:
        save_transactions([])
        return get_transactions()


def save_transactions(transactions):
    with lock:
        with open(file, 'w') as f:
            json.dump(transactions, f)


def add_transactions(new_transactions):
    transactions = get_transactions()
    try:
        transactions += new_transactions
    except TypeError:
        transactions += [new_transactions]
    save_transactions(transactions)


def get_incomplete(complete=True):
    transactions = get_transactions()
    incomplete = list(filter(lambda t: not t['Complete'], transactions))
    for t in incomplete:
        t['Complete'] = complete
    save_transactions(transactions)
    return incomplete


def get_html(classes='table'):
    return pd.concat([pd.DataFrame.from_dict({key: [value] for (key, value) in t.items()})
                      for t in get_transactions()], ignore_index=True).to_html(classes=classes)


def make_transaction(actor, amount, complete=False):
    return {'Actor': actor, 'Amount': amount, 'Complete': complete}


if __name__ == '__main__':
    test_transactions = [
        {'Actor': 'Grant Duffy', 'Amount': 1.0, 'Complete': False},
        {'Actor': 'Tom Duffy', 'Amount': 1.0, 'Complete': False},
        {'Actor': 'Grant Peltier', 'Amount': 1.0, 'Complete': False},
    ]

    add_transactions(test_transactions)
    print(get_html())
