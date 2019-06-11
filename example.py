#Created by Jonathan Woolf jwool003@ucr.edu

import gps
import serial.tools.list_ports

#create a list of accessible ports
port = ([comport.device for comport in serial.tools.list_ports.comports()])

#If no ports are accessible exit
if(len(port) == 0):
    print("Error: GPS unit not found!")
    exit()

#Open serial port
GPS = serial.Serial(port[0], baudrate = 9600)

#Verify port is open
if(GPS.is_open):
    print(GPS.name, "is open!")
    #Reset log and speed files every time the python script starts
    with open("log.txt", "w") as log:
        log.write("latitude, longitude, timestamp\n")
    with open("speed.txt", "w") as spd:
        spd.close()

#Infinite loop until KeyboardInterrupt is detected
try:
    while True:
        pos = gps.gpsData(GPS)
        latitude = pos[0]
        longitude = pos[1]
        MPH = pos[2]
        timestamp = pos[3]
        print(pos)

#'ctrl c' will close the serial port before exiting the program
except KeyboardInterrupt:
        GPS.close()
        if(GPS.is_open == False):
            print()
            print(GPS.name, "is closed!")
