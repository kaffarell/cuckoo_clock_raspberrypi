import clock
import sys
import os


while(True):
    print("What do you want to run?")
    print("(1)move clock motor")
    print("(2)move big disc")
    print("(3)move little disc")
    print("(4)move servo crane")
    print("(5)move servo tongue")
    print("(6)move hotel motor")
    print("(7)exit")
    selection = input()

    if selection == "1":
        clock.move_clockmotor()
    elif selection == "2":
        clock.move_bigdisc()
    elif selection == "3":
        clock.move_littledisc()
    elif selection == "4":
        os.system("sudo python3 \"/home/pi/cuckoo_clock_raspberrypi/servo_crane.py\"")
    elif selection == "5":
        os.system("sudo python3 \"/home/pi/cuckoo_clock_raspberrypi/servo_tongue.py\"")
    elif selection == "6":
        clock.move_hotelmotor()
    elif selection == "7":
        sys.exit()
