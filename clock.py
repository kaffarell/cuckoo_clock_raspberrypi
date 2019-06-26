import RPi.GPIO as GPIO
import time


def stepper(stepper_pins, delay):
    for pin in stepper_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    steps_seq = [[1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1]]

    for step in range(8):
        for pin in range(4):
            GPIO.output(stepper_pins[pin], steps_seq[step][pin])
        time.sleep(delay)

def main():
    #one revolution 512 (not approved)
    for i in range(512):
        stepper(stepper_pins, delay)

    GPIO.setmode(GPIO.BOARD)
    # stepper doesnt need resistor
    stepper_pins = [7,11,13,15]
    delay = 0.001

if __name__ == '__main__':
    main()

# https://elinux.org/RPi_GPIO_Interface_Circuits#Buttons_and_switches
# reed switch needs resistor!!
# avoid sensor needs resistor!!
# button needs resistor!!
# Servos:
# https://tutorials-raspberrypi.de/raspberry-pi-servo-motor-steuerung/
