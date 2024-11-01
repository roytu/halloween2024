
from threading import Thread
import subprocess
import sys
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from Adafruit_BBIO.SPI import SPI
from math import sin, pi
from time import sleep
from random import random

from svg_reader import get_osc_points

x_pwm = "P9_16"
y_pwm = "P8_13"
motor = "P8_11"
motion = "P8_12"
#lrc   = "P8_10"
#bclk  = "P8_12"
#din   = "P8_14"

osc_pwm_freq = 800000
sample_rate = 44100

def setup_pins():
    PWM.start(x_pwm, 100, osc_pwm_freq, 0)
    PWM.start(y_pwm, 50, osc_pwm_freq, 0)
    GPIO.setup(motor, GPIO.OUT)
    GPIO.setup(motion, GPIO.IN)
    #GPIO.setup(lrc, GPIO.OUT)
    #GPIO.setup(bclk, GPIO.OUT)
    #GPIO.setup(din, GPIO.OUT)

def cleanup():
    PWM.stop(x_pwm)
    PWM.stop(y_pwm)
    PWM.cleanup()
    GPIO.output(motor, GPIO.LOW)
    GPIO.output(lrc, GPIO.LOW)
    #spi.close()

def play_sound():
    # Pick a random voice to say
    fname = "audio" + str(int(random() * 6) + 1) + ".wav"
    subprocess.check_output("aplay " + fname, shell=True)

def animate():
    svg_fname = "furby1.svg"
    xs, ys = get_osc_points(svg_fname)
    N = len(xs)
    t = 0
    t_ = 0
    d = 0.000001
    while t_ < 0.03:
        x_value = xs[t]
        y_value = ys[t]
        set_x_value(x_value)
        set_y_value(y_value)
        sleep(d)
        t = (t + 1) % N
        t_ += d

# value is normalized 0 - 1
def set_x_value(value):
    value = max(min(value, 1), 0)
    PWM.set_duty_cycle(x_pwm, value * 100)

def set_y_value(value):
    value = max(min(value, 1), 0)
    PWM.set_duty_cycle(y_pwm, value * 100)

if __name__ == "__main__":
    setup_pins()

    try:
        while True:
            if GPIO.input(motion) > 0:
            #if True:
                t1 = Thread(target=play_sound, args=())
                t2 = Thread(target=animate, args=())
                GPIO.output(motor, 1)
                t1.start()
                t2.start()

                t1.join()
                t2.join()
                GPIO.output(motor, 0)
            sleep(1)
    except KeyboardInterrupt:
        pass
    cleanup()

    # Turn on motor
    #GPIO.output(motor, 0)
    #subprocess.check_output("aplay audio1.wav", shell=True)

