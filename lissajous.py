
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from math import sin, pi
from time import sleep
from random import random

from svg_reader import get_points

x_pwm = "P8_13"
y_pwm = "P9_16"

freq = 4000

def setup_pins():
    PWM.start(x_pwm, 100, freq, 0)
    PWM.start(y_pwm, 50, freq, 0)

def cleanup():
    PWM.stop(x_pwm)
    PWM.stop(y_pwm)
    PWM.cleanup()

# 7value is normalized 0 - 1
def set_x_value(value):
    value = max(min(value, 1), 0)
    PWM.set_duty_cycle(x_pwm, value * 100)

def set_y_value(value):
    value = max(min(value, 1), 0)
    PWM.set_duty_cycle(y_pwm, value * 100)

if __name__ == "__main__":
    setup_pins()
    xs, ys = get_points()
    N = len(xs)

    try:
        t = 0
        f = 100
        ratio = 2 / 3
        phase = pi / 4
        while True:
            x_value = sin(2 * pi * f * t + phase * t) / 2 + 0.5
            y_value = sin(2 * pi * f * ratio * t) / 2 + 0.5
            print(x_value)
            set_x_value(x_value)
            set_y_value(y_value)
            sleep(0.001)
            t += 0.001
    except KeyboardInterrupt:
        pass
    cleanup()
