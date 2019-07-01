import RPi.GPIO as GPIO
import time
import os
import logging
from stepper import Stepper
from subprocess import call
from servo import Servo

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
logging.basicConfig(level=logging.INFO, filename='raspi.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

stepper_pins_1 = [3, 4, 18, 27]
stepper_pins_2 = [23, 24, 10, 9]
delay = 0.001
GPIO.setup(2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


stepper1 = Stepper(stepper_pins_1, delay)
stepper2 = Stepper(stepper_pins_2, delay)
servo1 = Servo(17, 0)
servo1.set_to_zero()


def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return(temp.replace("temp=", ""))

def action():
    for counter_disc in  range(100):
        stepper2.step()
    counter_disc_failure = 0
    while(GPIO.input(11) == 1):
        counter_disc_failure += 1
        stepper2.step()
        if(counter_disc_failure > 1000):
            main()
    
    servo1.set_to_zero()   
    servo1.move(180, 0.01, 0)
    servo1.move(0, 0.01, 180)

    stepper1.hold()
    stepper2.hold()

    real_temp = measure_temp()[:3]
    if(float(real_temp) >= 70.0):
        call("sudo shutdown -h now", shell=True)
    
    logging.info("Temp: %s", str(real_temp))

    main()

def main():
    run_bool = True
    shutdown_counter = 0
    while(run_bool):
        time.sleep(0.5)
        if(GPIO.input(22) == 1):
            run_bool = False
        if(GPIO.input(26) == 1):
            shutdown_counter += 1
            print("hold")
            if(shutdown_counter >= 7):
                call("sudo shutdown -h now", shell=True)

    for counter_reed in range(100):
        stepper1.step()

    while(GPIO.input(2) == 0):
        stepper1.step()
    
    time.sleep(1)

    for counter_last_tick in range(43):
        stepper1.step()

    action()

if __name__ == '__main__':
    main()


GPIO.cleanup()

