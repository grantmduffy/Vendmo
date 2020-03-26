from lib_tft24T import TFT24T
import spidev
from RPi import GPIO
from PIL import Image, ImageFont, ImageDraw
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DC = 24
RST = 25
LED = 15

font = ImageFont.truetype('Roboto-Regular.ttf', size=30)

TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=True)
TFT.initLCD(DC, RST, LED)
TFT.clear()

d = TFT.draw()


def update(text):
    TFT.clear()
    d.text((10, 10), text, fill=(255, 255, 255), font=font)
    TFT.display()
