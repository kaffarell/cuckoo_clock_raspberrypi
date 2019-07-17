cockoo_clock_raspberrypi 

# Quick Start
Wiring:
https://docs.google.com/spreadsheets/d/1j9zD0qsTEPe5AXgHV7lEIsKP0KEnYZ0qRja9R-vCYoM/edit?usp=sharing

Clone the repo in:  
```
/home/pi/...
```

Standard Raspbian installation  
+  
For sound:  

```
sudo apt install mplayer
```

and optional: 

```
sudo apt install amixer
```

Execute the main program:
```
python clock.py
```

# Autostart with crontab

Execute:  
```
sudo crontab -e
```
and write to the file the following line:

```
@reboot sleep 5 && /usr/python /home/pi/cuckoo_clock_raspberrypi/clock.py >> /home/picuckoo_clock_raspberrypi/raspi.log 2>&1
```
to start the script everytime at startup
