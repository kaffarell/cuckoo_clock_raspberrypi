# 513 = 1 revolution

import RPi.GPIO as GPIO
import time
import logging as log

class Stepper:
       
    def __init__(self, stepper_pins, delay):
        self.stepper_pins = stepper_pins
        self.delay = delay

    def step(self):
        for pin in self.stepper_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        
        steps_seq = [[1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1]]

        for step in range(len(steps_seq)):
            for pin in range(4):
                GPIO.output(self.stepper_pins[pin], steps_seq[step][pin])
            time.sleep(self.delay)
    
    def hold(self):
        for pin in self.stepper_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        for pin1 in range(4):
            GPIO.output(self.stepper_pins[pin1], 0)
