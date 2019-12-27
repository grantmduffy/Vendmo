from threading import Lock
import pandas as pd
import json

lock = Lock()

file = 'transactions.json'


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


def add_transaction(t):
    transactions = get_transactions()
    transactions.append(t)
    save_transactions(transactions)


def get_html(classes='table'):
    transactions = get_transactions()
    if not transactions:
        return f'<table class="{classes}"></table>'
    return pd.concat([pd.DataFrame.from_dict({key: [value] for (key, value) in t.items()})
                      for t in transactions], ignore_index=True).to_html(classes=classes)


def make_transaction(actor, amount, complete=False):
    return {'Actor': actor, 'Amount': amount, 'Complete': complete}


if __name__ == '__main__':
    test_transactions = [
        {'Actor': 'Grant Duffy', 'Amount': 1.0, 'Complete': False},
        {'Actor': 'Tom Duffy', 'Amount': 1.0, 'Complete': False},
        {'Actor': 'Grant Peltier', 'Amount': 1.0, 'Complete': False},
    ]
    for t in test_transactions:
        add_transaction(t)
    print(get_html())
