#!/usr/local/bin/python
import RPi.GPIO as GPIO
import time
import os
import logging
from stepper import Stepper
from subprocess import call

visitors = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logging.basicConfig(level=logging.DEBUG, filename='/home/pi/cuckoo_clock/raspi.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')


stepper_pins_1 = [3, 4, 18, 27]
stepper_pins_2 = [23, 24, 10, 9]
stepper_delay = 0.001

# reed sensor clock
GPIO.setup(2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# reed sensor disc
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# start button
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
# shutdown button
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


stepper1 = Stepper(stepper_pins_1, stepper_delay)
stepper2 = Stepper(stepper_pins_2, stepper_delay)

def increase_visitors():
    global visitors
    visitors += 1
    print(visitors)


def get_temp():
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
            stepper2.hold()
            main()
    stepper2.hold()
    

    # start extern file to move servos
    os.system("sudo python \"/home/pi/cuckoo_clock/move_servo.py\"")
    
    # set jack as output and play file
    os.system("amixer -c 0 cset numid=3 1 -q")
    os.system("mplayer /home/pi/cuckoo_clock/kuckuck.wav > /dev/null 2>&1")

    
    # shutdown pi when temperature is over 75
    real_temp = get_temp()[:3]
    if(float(real_temp) >= 75.0):
        logging.error("rasperrypi overheating!")
        #call("sudo /sbin/shutdown -h now")
        os.system("/sbin/shutdown -h now")
    
    logging.info("Temp: %s", str(real_temp))
    main()

def main():
    global visitors
    main_run_bool = True
    shutdown_counter = 0
    
    while(main_run_bool):
        time.sleep(0.5)
        # start button
        if(GPIO.input(22) == 1):
            increase_visitors()
            main_run_bool = False
        # shutdown button
        if(GPIO.input(26) == 1):
            shutdown_counter += 1
            print("hold")
            if(shutdown_counter == 7):
                # when shutting down writing visitors to file
                with open("/home/pi/cuckoo_clock/visitors", "a") as f:
                    f.write(str(visitors))
                    f.write("\n")
                
                logging.info("shutdown raspberry pi")
                os.system("/sbin/shutdown -h now")
                

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

    for clock_last_tick in range(43):
        stepper1.step()

    action()

if __name__ == '__main__':
    main()


