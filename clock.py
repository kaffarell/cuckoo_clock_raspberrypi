#!/usr/bin/python3
import logging as log
import os
import threading
import time

import RPi.GPIO as GPIO
from stepper import Stepper

visitors = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

log.basicConfig(level=log.DEBUG, filename='/home/pi/cuckoo_clock_raspberrypi/raspi.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

log.info("startup raspberry pi")

clock_motor_pins = [3, 4, 18, 27]
disk_motor_pins = [23, 24, 10, 9]
bigdisc_motor_pins = [21, 20, 16, 12]
hotel_motor_pins = [19, 6, 5, 7]


# reed sensor big disc
GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# reed sensor hotel
GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# reed sensor clock
GPIO.setup(2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# reed sensor disc
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# start button
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
# shutdown button
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


clock_motor = Stepper(clock_motor_pins, 0.003)
disk_motor = Stepper(disk_motor_pins, 0.003)
bigdisc_motor = Stepper(bigdisc_motor_pins, 0.001)
hotel_motor = Stepper(hotel_motor_pins, 0.001)

clock_motor.hold()
disk_motor.hold()
bigdisc_motor.hold()
hotel_motor.hold()



def get_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return(temp.replace("temp=", ""))


def move_clock_motor():
    print("OK")
    # move clock
    for counter_reed in range(100):
        clock_motor.step("low-speed")
    
    clock_counter_failure = 0
    while(GPIO.input(2) == 0):
        clock_counter_failure += 1
        clock_motor.step("high-speed")
        if(clock_counter_failure >= 1000):
            log.error("reed sensor clock failed!")
            clock_motor.hold()
            break 
    time.sleep(1)
    # clock last 5 minutes
    for clock_last_tick in range(43):
        clock_motor.step("high-speed")
    clock_motor.hold()


def move_little_disc():
    # move little disc (unesco)
    for counter_disc in  range(100):
        disk_motor.step("high-speed")
    counter_disc_failure = 0
    while(GPIO.input(11) == 1):
        counter_disc_failure += 1
        disk_motor.step("high-speed")
        if(counter_disc_failure >= 1000):
            log.error("reed sensor disc failed!")
            disk_motor.hold()
            break  
        disk_motor.hold()
    
def move_bigdisc():
    # move big disc (cars)
    bigdisc_failure = 0
    for counter_bigdisc in  range(100):
        bigdisc_motor.step("high-speed")
    bigdisc_failure = 0
    while(GPIO.input(14) == 0):
        bigdisc_failure += 1
        bigdisc_motor.step("high-speed")
        if(bigdisc_failure >= 1000):
            log.error("reed sensor bigdisc failed!")
            bigdisc_motor.hold()
            break       
    bigdisc_motor.hold()


def move_hotelmotor():
    # move hotel triangle
    hotel_motor_failure = 0
    for counter_hotel_motor in range(100):
        hotel_motor.step("high-speed")
    hotel_motor_failure = 0
    while(GPIO.input(15) == 0):
        hotel_motor_failure += 1
        hotel_motor.step("high-speed")
        if(hotel_motor_failure > 4000):
            log.error("reed sensor hotel motor failed!")
            hotel_motor.hold()
            break
    hotel_motor.hold()


def action():

    clock_motor_thread = threading.Thread(target=move_clock_motor)
    clock_motor_thread.start()
    

    # set jack as output and play vielen dank ... sound
    os.system("amixer -c 0 cset numid=3 1 -q &")
    os.system("ffplay /home/pi/cuckoo_clock_raspberrypi/vielen_dank.mp3 -autoexit > /dev/null 2>&1 &")

    time.sleep(2)

    move_little_disc()

    # set jack as output and play traffic noise
    os.system("amixer -c 0 cset numid=3 1 -q &")
    os.system("ffplay /home/pi/cuckoo_clock_raspberrypi/traffic_noise.mp3 -autoexit > /dev/null 2>&1 &")

    
    move_bigdisc()
    

    # start extern file to move servos of crane
    os.system("sudo python3 \"/home/pi/cuckoo_clock_raspberrypi/servo_crane.py\"")

    move_hotelmotor()
    
    # move the tongue with extern file
    os.system("sudo python3 \"/home/pi/cuckoo_clock_raspberrypi/servo_tongue.py\"")

    # shutdown pi when temperature is over 75
    real_temp = get_temp()[:3]
    if(float(real_temp) >= 75.0):
        log.error("rasperrypi overheating!")
        os.system("/sbin/shutdown -h now")
    
    log.info("Temp: %s", str(real_temp))
    main()

def main():
    global visitors
    # TODO: remove at release !!
    print(visitors)
    main_run_bool = True
    shutdown_counter = 0
    
    while(main_run_bool):
        time.sleep(0.5)

        # start button
        if(GPIO.input(22) == 1):
            visitors += 1
            main_run_bool = False

        # shutdown button
        if(GPIO.input(26) == 1):
            shutdown_counter += 1
            print("hold")
            if(shutdown_counter == 7):
                # when shutting down writing visitors to file
                try:
                    with open("/home/pi/cuckoo_clock_raspberrypi/visitors", "a") as f:
                        f.write(str(visitors))
                        f.write("\n")
                except Exception as e:
                    log.error("%s", e)
                
                log.info("shutdown raspberry pi")
                os.system("sudo /sbin/shutdown -h now")
                
    action()

if __name__ == '__main__':
    main()
