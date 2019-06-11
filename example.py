#Created by Jonathan Woolf jwool003@ucr.edu

import gps

port = gps.serialPortInit()

#Infinite loop until KeyboardInterrupt is detected
try:
    while True:
        data = gps.gpsData(port)
        #Unused - Just an example of how to grab data from the function
        latitude = data[0]
        longitude = data[1]
        MPH = data[2]
        timestamp = data[3]
        print(data)

#'ctrl c' will close the serial port before exiting the program
except KeyboardInterrupt:
        port.close()
        if(port.is_open == False):
            print()
            print(port.name, "is closed!")
