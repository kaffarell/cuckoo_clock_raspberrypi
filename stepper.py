import RPi.GPIO as GPIO
import time
import logging as log

class Stepper:
       
    def __init__(self, stepper_pins, delay):
        self.stepper_pins = stepper_pins
        self.delay = delay

    def step(self):
        for pin in self.stepper_pins:
            try:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, 0)
            except Exception as e:
                log.error("%s", e)
                log.error("Pin %d not working", pin)

        steps_seq = [[1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1]]

        for step in range(8):
            for pin in range(4):
                GPIO.output(self.stepper_pins[pin], steps_seq[step][pin])
            time.sleep(self.delay)
    def hold(self):
        for pin1 in range(4):
            GPIO.output(self.stepper_pins[pin1], 0)
