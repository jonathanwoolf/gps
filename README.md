# Author: Jonathan Woolf jwool003@ucr.edu

This code reads data from the serial port connected to your <a href="https://www.amazon.com/HiLetgo-G-Mouse-GLONASS-Receiver-Windows/dp/B01MTU9KTF/ref=sr_1_8?keywords=gps+usb&qid=1560277792&s=gateway&sr=8-8">GPS device</a>,
for example "ttyACM0", and calls the function "gpsData()" which reads the serial
port to return latitude, longitude, MPH, and a timestamp. The function also
outputs data to pos.txt, log.txt, and speed.txt.

For convenience, the function is called in an infinite loop nested in a
try / except block and the return statement is printed to terminal. Type 'ctrl c'
to guarantee that the serial port is closed when you end the program

## Give yourself permanent access to the port:
#### Discover which serial port is in use
python -m serial.tools.list_ports
#### navigate to rules.d directory
cd /etc/udev/rules.d
#### create a new rule file
sudo touch my-newrule.rules
#### open the file
sudo vim my-newrule.rules
#### add the following
KERNEL=="ttyACM0", MODE="0666"
