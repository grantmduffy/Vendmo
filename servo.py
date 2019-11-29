from sys import platform
from time import sleep

serovo_pin = 18
open_pos, closed_pos = 1, 0.5
delay = 1.0

if platform == 'linux':
    import wiringpi as wp
    wp.wiringPiSetupGpio()
    wp.pinMode(serovo_pin, wp.GPIO.PWM_OUTPUT)
    wp.pwmSetMode(wp.GPIO.PWM_MODE_MS)
    wp.pwmSetClock(192)
    wp.pwmSetRange(2000)


def move_servo_to(pos):
    if platform == 'linux':
        wp.pwmWrite(serovo_pin, int(pos * 200 + 50))
    else:
        print('Move servo to {pos}')


def dispense_beer():
    move_servo_to(open_pos)
    sleep(delay)
    move_servo_to(closed_pos)
