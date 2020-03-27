from lib_tft24T import TFT24T, Buffer
import spidev
from RPi import GPIO
from PIL import Image, ImageFont, ImageDraw
from settings import Settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

s = Settings()

DC = 24
RST = 25
LED = 15

font = ImageFont.truetype('Roboto-Regular.ttf', size=20)

TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=True)
TFT.initLCD(DC, RST, LED)
TFT.clear()

d = TFT.draw()
idle_phrase = f'Venmo {s.venmo_user} ${s.price:.2f}\nwith "{s.user_phrase}" in the caption'
qr_code = None
scale = 3


def load_qr():
    global qr_code
    qr_code = Image.open('qr.png')
    qr_code = qr_code.resize((qr_code.size[0] // scale, qr_code.size[1] // scale))


def idle_screen():
    TFT.clear()
    d.text((10, 10), idle_phrase, fill=(255, 255, 255), font=font)
    if qr_code is not None:
        Buffer.paste(qr_code, (40, 10))
    TFT.display()


def dispense_screen(actor):
    TFT.clear()
    d.text((10, 10), f'This beer is for\n"{actor}"', fill=(255, 255, 255), font=font)
    TFT.display()
