#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Uses device location to generate an html google map
GPL 3.0
"""

# Built-in/Generic Imports
import os
# […]

# Own modules
import gps
# […]

# Google's module (provided because pip doesn't have it)
import pygmaps
# […]

__author__ = "Jonathan Woolf"
__credits__ = "Jonathan Woolf, AnkitRai01, Google"
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Jonathan Woolf"
__email__ = "jwool003@ucr.edu"
__status__ = 'alpha'

mode = input("Please input mode: walking / vehicle\n")

port = gps.serialPortInit()
data = gps.gpsData(port)
latitude = data[0]
longitude = data[1]
print(data)

if(os.path.exists('map.html')):
    os.remove("map.html")

map = pygmaps.pygmaps(data[0],data[1],14)
map.addpoint(data[0],data[1],"# FF0000")
map.draw('map.html')

# Infinite loop until KeyboardInterrupt is detected
try:
    while True:
        data = gps.gpsData(port)
        if(mode == 'w' or mode == 'W' or mode == "walking" or "Walking"):
            if((data[2] > 0.1) and (abs(latitude - data[0]) > .001 or abs(longitude - data[1]) > .001)):
                map.addpoint(data[0],data[1],"# FF0000")
                # list of coordinates
                path = [(latitude, longitude),
                        (data[0], data[1])]
                # draw a line in b / w the given coordinates
                # 1st argument is list of coordinates
                # 2nd argument is colour of the line
                print("New coordinate registered!")
                map.addpath(path, " 0000FF")
                map.draw('map.html')
                print(data)
                latitude = data[0]
                longitude = data[1]
        if(mode == 'v' or mode == 'V' or mode == "vehicle" or "Vehicle"):
            if((data[2] > 0.1) and (abs(latitude - data[0]) > .01 or abs(longitude - data[1]) > .01)):
                map.addpoint(data[0],data[1],"# FF0000")
                # list of coordinates
                path = [(latitude, longitude),
                        (data[0], data[1])]
                # draw a line in b / w the given coordinates
                # 1st argument is list of coordinates
                # 2nd argument is colour of the line
                print("New coordinate registered!")
                map.addpath(path, " 0000FF")
                map.draw('map.html')
                print(data)
                latitude = data[0]
                longitude = data[1]

#'ctrl c' will close the serial port before exiting the program
except KeyboardInterrupt:
        port.close()
        if(port.is_open == False):
            print()
            print(port.name, "is closed!")
