import RPi.GPIO as GPIO
import time
import logging
import numpy


class Servo:
    servo_letter = ["a", "b", "c", "d", "e", "f"]
    def __init__(self, servo_pin, servo_letter_index):
        self.servo_pin = servo_pin
        self.servo_letter_index = servo_letter_index
              
        try:
            GPIO.setup(servo_pin, GPIO.OUT)
            self.servo_letter[servo_letter_index] = GPIO.PWM(servo_pin, 50)
        except Exception as e:
            logging.error("%s", e)
            logging.error("Pin %s not working", servo_pin)
                 

    def start(self):
        self.servo_letter[self.servo_letter_index] = GPIO.PWM(self.servo_pin, 50)
        self.servo_letter[self.servo_letter_index].start(2.5)
        time.sleep(3)


    def move(self, position):
        self.servo_letter[self.servo_letter_index].ChangeDutyCycle(position)
        time.sleep(3)
        
        #for i in numpy.arange(act_pos, position, 0.001):
            #self.servo_letter[self.servo_letter_index].ChangeDutyCycle(i)
            #time.sleep(speed)

    def stop(self):
        self.servo_letter[self.servo_letter_index].stop()

    def set_to_zero(self):
       self.servo_letter[self.servo_letter_index].ChangeDutyCycle(2.5)
       time.sleep(1.5)

