#Created by Jonathan Woolf jwool003@ucr.edu

#Global scope
startTime = -1

#Pass in UTC string, output PT string
def utcToPT(utc):
    #PT is 17hours ahead of UTC
    PT = 170000 + int(float(utc))
    if(PT >= 240000):
        PT = PT - 240000
        if(PT < 10000):
            PT = "00" + str(PT)
        elif(PT < 100000):
            PT = "0" + str(PT)
    return(str(PT))

#Pass in DMS and direction, output DD
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

def gpsData(GPS):#, startTime = -1):
    global startTime
    data = [-1] * 3
    sec = -1

    while(data[0] != "$GPGGA"):
        line = GPS.readline()
        data = line.decode().split(",")

    if(data[0] == "$GPGGA"):
        #Fix quality: 0 = invalid
        if(data[6] != "0"):
            #data[1] returns time in UTC, convert it to PT and create a timestamp
            PT = utcToPT(data[1])
            hour = PT[0] + PT[1]
            min = PT[2] + PT[3]
            sec = PT[4] + PT[5]
            timestamp = hour + ':' + min + ':' + sec
            if(startTime == -1):
                startTime = int(sec)

    while(data[0] != "$GPRMC"):
        line = GPS.readline()
        data = line.decode().split(",")

    if(data[0] == "$GPRMC"):
        #Status A=active or V=Void
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
            if(abs(int(sec) - startTime) == 0):
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
