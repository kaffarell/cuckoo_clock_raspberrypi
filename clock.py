import RPi.GPIO as GPIO
import time
import os
import logging
from pygame import mixer
from stepper import Stepper
from subprocess import call
from servo import Servo



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logging.basicConfig(level=logging.DEBUG, filename='raspi.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')


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
servo1.start()

def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return(temp.replace("temp=", ""))

def action():
    stepper1.hold()
    for counter_disc in  range(100):
        stepper2.step()
    counter_disc_failure = 0
    while(GPIO.input(11) == 1):
        counter_disc_failure += 1
        stepper2.step()
        if(counter_disc_failure > 1000):
            main()

    servo1.set_to_zero()
    servo1.move(12.5)
    servo1.move(2.5)
    servo1.move(12.5)
    servo1.move(2.5)
    stepper2.hold()
    
    mixer.init()
    sound = mixer.Sound("excavator_sound.wav")
    sound.play()
    

    real_temp = measure_temp()[:3]
    if(float(real_temp) >= 75.0):
        logging.error("rasperrypi overheating!")
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
                logging.info("shutdown raspberry pi")
                call("sudo shutdown -h now", shell=True)

    for counter_reed in range(100):
        stepper1.step()
    
    clock_counter_failure = 0
    while(GPIO.input(2) == 0):
        clock_counter_failure += 1
        stepper1.step()
        if(clock_counter_failure >= 512):
            logging.error("clock sensor failed!")
            stepper1.hold()
            main()
    
    time.sleep(1)

    for counter_last_tick in range(43):
        stepper1.step()

    action()

if __name__ == '__main__':
    main()

servo1.stop()
GPIO.cleanup()

