
'''
README:
Author: Jonathan Woolf jwool003@ucr.edu

This code reads data from the linux serial port connected to your GPS device,
for example "ttyACM0", and calls the function "gpsData()" which reads the serial
port to return latitude, longitude, MPH, and a timestamp. The function also
outputs data to pos.txt, log.txt, and speed.txt.

For convenience, the function is called in an infinite loop nested in a
try / except block and the return statement is printed to terminal. Type 'ctrl c'
to guarantee that the serial port is clsoed when you end the program

Give yourself permanent access to the port:

python -m serial.tools.list_ports
# navigate to rules.d directory
cd /etc/udev/rules.d
#create a new rule file
sudo touch my-newrule.rules
# open the file
sudo vim my-newrule.rules
# add the following
KERNEL=="ttyACM0", MODE="0666"
'''

import serial
import serial.tools.list_ports
import time

def utcToPT(utc):
    PT = 170000 + int(float(utc))
    if(PT >= 240000):
        PT = PT - 240000
        if(PT < 10000):
            PT = "00" + str(PT)
    return(str(PT))

def decimalDegrees(dms, direction):
    DD = int(float(dms)/100)
    SS = float(dms) - DD * 100

    DD = round(DD + SS/60, 7)
    tmp1 = len(str(int(DD)))
    tmp2 = len(str(DD))

    #Rounds DD (decimal degrees) for more consistent values
    if((tmp1 == 1 and tmp2 < 9) or (tmp1 == 2 and tmp2 < 10) or (tmp1 == 3 and tmp2 < 11)):
        DD = round(DD +  .0000001, 7)
    #If South latitude is negative / If West longitude is negative
    if(direction == "S" or direction == "W"):
        DD = DD * -1
    return(DD)

def gpsData(GPS, startTime = -1):
    data = [-1] * 3
    sec = -1
    timestamp =  time.strftime('%H:%M:%S') #"00:00:00" #If time library is unavailable
    while(data[0] != "$GPRMC"):
        line = GPS.readline()
        data = line.decode().split(",")
        #find pacific time from UTC & create timestamp
        if(data[0] == "$GPGGA"):
            PT = utcToPT(data[1])
            hour = PT[0] + PT[1]
            min = PT[2] + PT[3]
            sec = PT[4] + PT[5]
            timestamp = hour + ':' + min + ':' + sec

    if(data[0] == "$GPRMC"):
        #A means that the GPS is updating properly and returning a real value
        if(data[2] == "A"):
            #Convert from DMS (degrees, minutes, seconds) to DD (decimal degrees)
            latitude = decimalDegrees(data[3], data[4])
            longitude = decimalDegrees(data[5], data[6])
            #1 knot = 1.15078 miles per hour
            mph = round(1.15078 * float(int(float(data[7]))), 1)

            #write MPH and timestamp to speed.txt file whenever MPH >= 0.1
            if(float(mph) >= 0.1):
                with open("speed.txt", "a") as spd:
                    spd.write("MPH: " + str(mph) + ", Timestamp: " + timestamp + "\n")
            #write latitude, longitude to .txt file
            with open("pos.txt", "w") as pos:
                pos.write("latitude, longitude, timestamp\n" + str(latitude)
                + ", " + str(longitude) +  ", " + timestamp + "\n")
            #write latitude, longitude, and timestamp to log.txt file every 60 seconds
            if((startTime != -1) and (abs(int(sec) - startTime) == 0)):
                with open("log.txt", "a") as log:
                    log.write(str(latitude) + ", " + str(longitude) + ", " + timestamp + "\n")
            #return latitude, longitude, and timestamp
            return(latitude, longitude, mph, timestamp)
        else:
            print("Error: satellites not found. Dislplaying last known coordinates:")
            with open("pos.txt", "r") as pos:
                backup = pos.read().split('\n')
                backup = backup[1].split(", ")
                return(float(backup[0]), float(backup[1]), 'N/A', backup[2])

#create a list of accessible ports
port = ([comport.device for comport in serial.tools.list_ports.comports()])

#If no ports are accessible exit
if(len(port) == 0):
    print("Error: GPS unit not found!")
    exit()

#Open GPS port
GPS = serial.Serial(port[0], baudrate = 9600)

#Verify port is open
if(GPS.is_open):
    print(GPS.name, "is open!")
    #Reset log every time the python script starts
    with open("log.txt", "w") as log:
        log.write("latitude, longitude, timestamp\n")
    with open("speed.txt", "w") as spd:
        spd.close()
        #.write("latitude, longitude, timestamp\n")

#Set startTime
startTime = int(time.strftime('%S'))

#Infinite loop until KeyboardInterrupt is detected
try:
    while True:
        pos = gpsData(GPS, startTime)
        print(pos)
        #time.sleep(5) #Sleep for better power reserve if needed

#'ctrl c' will close the serial port before exiting the program
except KeyboardInterrupt:
        GPS.close()
        if(GPS.is_open == False):
            print()
            print(GPS.name, "is closed!")
