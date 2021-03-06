from sys import platform
from time import sleep

servo_pin = 12
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
    import wiringpi as wp
    wp.wiringPiSetupGpio()
    wp.pinMode(servo_pin, wp.GPIO.PWM_OUTPUT)
    wp.pwmSetMode(wp.GPIO.PWM_MODE_MS)
    wp.pwmSetClock(192)
    wp.pwmSetRange(2000)
    move_servo_to(closed_pos)
