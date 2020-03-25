from lib_tft24T import TFT24T
import spidev
from RPi import GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DC = 24
RST = 25
LED = 15

TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=False)
TFT.initLCD(DC, RST, LED)
draw = TFT.draw()

TFT.clear((0, 255, 0))
