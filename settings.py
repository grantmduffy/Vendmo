from werkzeug.security import generate_password_hash, check_password_hash
from json import dumps, loads
from sys import platform


class Settings:

    defaults = {
        'password': generate_password_hash('Vendmo', method='sha256'),
        'email_address': '',
        'email_password': ''
    }
    file = 'settings.json'

    def __init__(self):
        if platform == 'linux':
            self.file = '/home/pi/' + self.file

    def _load(self):
        try:
            with open(self.file, 'r') as f:
                return loads(f.read())
        except FileNotFoundError:
            with open(self.file, 'w') as f:
                f.write(dumps(self.defaults))
            return self._load()

    def __getattr__(self, item):
        return self._load()[item]

    def __setattr__(self, key, value):
        s = self._load()
        s[key] = value
        with open(self.file, 'w') as f:
            f.write(dumps(s))