# Author: Jonathan Woolf jwool003@ucr.edu

This code reads data from the serial port connected to your <a href="https://www.amazon.com/HiLetgo-G-Mouse-GLONASS-Receiver-Windows/dp/B01MTU9KTF/ref=sr_1_8?keywords=gps+usb&qid=1560277792&s=gateway&sr=8-8">GPS device</a>, for example "ttyACM0", and calls the function "gpsData()", which returns latitude, longitude, MPH, and a timestamp. The function also outputs data to pos.txt, log.txt (every 60 seconds), and speed.txt (when speed > 0 MPH).

 
For convenience, the function in the example script is called whithin an infinite loop that is nested in a try / except block and the return statement is printed to terminal. Type 'ctrl c' to guarantee that the serial port is closed when you end the program.

## Give yourself permanent access to the port:
    # Discover which serial port is in use
    python -m serial.tools.list_ports
    # Navigate to rules.d directory
    cd /etc/udev/rules.d
    # Create a new rule file
    sudo touch my-newrule.rules
    # Open the file
    sudo vim my-newrule.rules
    # Add the following:
    #KERNEL=="ttyACM0", MODE="0666"

## Tutorial:
#### Dependencies
    pip install PYserial
#### Access gpsData()
    import gps
    port = gps.serialPortInit()
    gps.gpsData(port)
#### Run example script
    python example.py
