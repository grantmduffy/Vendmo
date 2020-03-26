from abc import ABC
from settings import Settings
import imaplib
import quopri
from html.parser import HTMLParser
from time import sleep
from sys import platform
if platform == 'linux':
    import wiringpi as wp
    from display import update


class EmailParser(HTMLParser, ABC):

    def __init__(self):
        super(EmailParser, self).__init__()
        self.section = None
        self.values = {}
        self.level = 0
        self.actor = ''
        self.recipient = ''
        self.action = ''
        self.amount = 0
        self.note = ''

    def __str__(self):
        return f'{self.actor} {self.action} {self.recipient} ${self.amount} for {self.note}'

    def feed(self, data):
        super(EmailParser, self).feed(data)
        try:
            self.actor = self.values['actor name'][0]
            self.action = self.values['action'][0]
            self.recipient = self.values['recipient name'][0]
            self.note = self.values['note'][0]
            self.amount = float(self.values['amount'][0][3:].replace(',', ''))
        except KeyError:
            print('Email receipt not read...')

    def handle_starttag(self, tag, attrs):
        self.level += 1

    def handle_endtag(self, tag):
        self.level -= 1
        if self.level == 0:
            self.section = None

    def handle_data(self, data):
        if self.section is not None and not data.isspace() and self.level > 0:
            if self.section not in self.values:
                self.values[self.section] = []
            self.values[self.section].append(data.strip())

    def handle_comment(self, data):
        self.section = data.strip()
        self.level = 0


servo_pin = 18
open_pos, closed_pos = 0.0, 1.0
motor_delay = 0.5
grab_delay = 5.0


def move_servo_to(pos):
    if platform == 'linux':
        wp.pwmWrite(servo_pin, int(pos * 200 + 50))
    else:
        print(f'Move servo to {pos}')


def dispense_beer():
    move_servo_to(open_pos)
    sleep(motor_delay)
    move_servo_to(closed_pos)
    sleep(grab_delay)


if platform == 'linux':
    wp.wiringPiSetupGpio()
    wp.pinMode(servo_pin, wp.GPIO.PWM_OUTPUT)
    wp.pwmSetMode(wp.GPIO.PWM_MODE_MS)
    wp.pwmSetClock(192)
    wp.pwmSetRange(2000)
    move_servo_to(closed_pos)

s = Settings()

mail = imaplib.IMAP4_SSL(s.imap_server)
mail.login(s.email_address, s.email_password)
mail.select('inbox')


while True:
    try:
        _, ids = mail.search(None, '(OR FROM venmo@venmo.com FROM grantmduffy@gmail.com '
                                   f'SUBJECT "paid you" UNSEEN)')
        for id in ids[0].split():
            _, data = mail.fetch(id, '(BODY[TEXT])')
            data = quopri.decodestring(data[0][1]).decode('utf-8')
            p = EmailParser()
            p.feed(data)
            print(p)
            if p.amount >= s.price and s.user_phrase.lower() in p.note.lower():
                print(f'DISPENSE BEER FOR "{p.actor}"')
                update(f'Dispense beer for:\n"{p.actor}"')
                dispense_beer()
        sleep(5)
    except Exception as e:
        print(e)
