from lib_tft24T import TFT24T
import spidev
from RPi import GPIO
from PIL import Image, ImageFont, ImageDraw
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from PIL import ImageDraw

DC = 24
RST = 25
LED = 15

TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=True)
TFT.initLCD(DC, RST, LED)
TFT.clear((0, 0, 0))

d = TFT.draw()
d.text((10, 10), 'Hello World', fill=255)
TFT.display()
