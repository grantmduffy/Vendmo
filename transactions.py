from threading import Lock
from sys import platform
import pickle
import pandas as pd

lock = Lock()

file = 'transactions.pkl'
if platform == 'linux':
    file = '/home/pi/' + file


def get_transactions():
    try:
        with lock:
            return pd.read_pickle(file)
    except FileNotFoundError:
        save_transactions(pd.DataFrame(columns=['Actor', 'Amount', 'Completed']))
        return get_transactions()


def save_transactions(transactions):
    with lock:
        pd.to_pickle(transactions, file)


def add_transactions(transactions):
    df = get_transactions()
    df = df.append(pd.DataFrame(transactions, columns=['Actor', 'Amount', 'Completed']))
    with lock:
        df.to_pickle(file)


def get_incomplete(complete=True):
    df = get_transactions()
    incomplete = df[df['Completed'] == False]
    df['Completed'][df['Completed'] == False] = complete
    save_transactions(df)
    return incomplete


if __name__ == '__main__':
    df = pd.DataFrame([['Grant', 1.0, False], ['Sam', 1.0, True]],
                      columns=['Actor', 'Amount', 'Completed'])
    print(df)
    # df['Completed'][df['Completed'] == False] = True
    save_transactions(df)
    print(df)