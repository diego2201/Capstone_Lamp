import sys

import aioble
import bluetooth
import machine
import uasyncio as asyncio
from micropython import const

import utime
import math
from time import sleep

import time
from sys import stdin
import uselect

from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd

#Import for I2C connection with LCD Display
i2c = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

fileName = "data.txt"

"""
Function to save data to specified file 
"""
async def saveFile(data):
    with open(fileName, "w") as file:
        file.write(data + "\n")

"""
Function to read file from serial input calls the saveFile function
to save 
"""    
async def flag():  
    while True:
        selectResult = uselect.select([stdin], [], [], 0)
        val = ''
        while selectResult[0]:
            inputChar = stdin.read(1)
            if inputChar != ',':
                val += inputChar
            else:
                await saveFile(val)
                val =''
            selectResult = uselect.select([stdin], [], [], 0)
        await asyncio.sleep(0.1)

# Defines UART pins and baud rate
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

# Defines global variables where we will store our NMEA data
latitude = 0.0
longitude = 0.0
date = ""
time = ""
formatted_date = ""
formatted_time = ""

cardDirection = ""
cardDirection2 = ""

# Flag that stores our 
locFlag = 0

closest_city = None
closest_landmark = None

# Defines a list of major cities and their coords (latitude, longitude)
cities = {
    "New York City, USA": (40.7128, -74.0060, 'a'),
    "San Francisco, USA": (37.7749, -122.4194, 'b'),
    "Norman, Oklahoma, USA": (35.2220, -97.4395, 'c'),
    "Los Angeles, USA": (34.0522, -118.2437, 'd'),
    "Chicago, USA": (41.8781, -87.6298, 'e'),
    "London, United Kingdom": (51.5074, -0.1278, 'f'),
    "Tokyo, Japan": (35.682839, 139.759455, 'g'),
    "Dubai, United Arab Emirates": (25.276987, 55.296249, 'h'),
    "Paris, France": (48.8566, 2.3522, 'i'),
    "Sydney, Australia": (-33.8651, 151.2099, 'j'),
    "University of Oklahoma, USA": (20.6843, -88.5678, 'k'),
}

# Defines a list of major landmarks and their coords (latitude, longitude)
landmarks = {
    "Statue of Liberty, USA": (40.6892, -74.0445),
    "Golden Gate Bridge, USA": (37.8199, -122.4783),
    "Eiffel Tower, France": (48.858844, 2.294351),
    "Big Ben, United Kingdom": (51.5007, -0.1246),
    "Tokyo Tower, Japan": (35.6586, 139.7454),
    "Hagia Sophia, Turkey": (41.0082, 28.9784),
    "Burj Khalifa, United Arab Emirates": (25.276987, 55.296249),
    "Marina Bay Sands, Singapore": (1.2835, 103.8595),
    "Pyramids of Giza, Egypt": (29.9792, 31.1344),
    "Sydney Opera House, Australia": (-33.8568, 151.2153),
    "Taj Mahal, India": (27.1751, 78.0421),
    "University of Oklahoma, USA": (20.6843, -88.5678)
}

"""
Function to calculate the distance between two sets of coordinates using Haversine formula
"""
def calcDist(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Radius of the Earth in kilometers

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

"""
Function to find the closest city
"""
def findCity(latitude, longitude, cities):
    global locFlag
    
    # Conditional statement to send error flag 
    if (latitude == 0.0) and (longitude == 0.0):
        locFlag = '!'
        closest_city = None
        return closest_city
    
    closest_city = None
    closest_distance = float("inf")

    for city, coordinates in cities.items():
        city_latitude, city_longitude, flag = coordinates  # Unpacks the coordinates including the flag
        distance = calcDist((latitude, longitude), (city_latitude, city_longitude))
        if distance < closest_distance:
            closest_city = city
            locFlag = flag
            closest_distance = distance

    return closest_city


"""
Function to find the closest landmark
"""
def findLandmark(latitude, longitude, landmarks):
    if (latitude == 0.0) and (longitude == 0.0):
        closest_landmark = None
        return closest_landmark
    
    closest_landmark = None
    closest_distance_landmark = float("inf")

    for landmark, coordinates in landmarks.items():
        distance = calcDist((latitude, longitude), coordinates)
        if distance < closest_distance_landmark:
            closest_landmark = landmark
            closest_distance_landmark = distance

    return closest_landmark

"""
Function to convert the coord from NMEA formatting to 
traditional mm.ss
"""
def convertCoords(coord, direction):
    degree = int(coord // 100)
    minutes = coord % 100
    
    decimal = minutes / 60
    
    finalCoord = degree + decimal
    
    if direction == 'S':
        finalCoord = -finalCoord
    if direction == 'W':
        finalCoord = -finalCoord
    
    return finalCoord

"""
Function to read in GPS data from NMEA 
"""
async def getNMEA():
    # Calls in all the global variables needed to store the information and continually update 
    global latitude, longitude, formatted_date, formatted_time, cardDirection, cardDirection2, closest_city, closest_landmark
    
    # While loop to continually read from GPS receiver 
    while True:
        data = uart.readline()
        
        # As long as there is data to read
        if data:
            try:
                data = data.decode('utf-8').strip()
            except UnicodeError:
                continue  # Ignores the problematic character and continue

            # Checks if the sentence starts with '$GP'
            if data.startswith('$GP'):
                parts = data.split(',') # Splits the NMEA sentence into a list 

                if parts[0] == '$GPGGA':
                    if len(parts) >= 10:
                        try:     
                            # Stores the respective variables from the list
                            latitude = convertCoords(float(parts[2]), parts[3])
                            longitude = convertCoords(float(parts[4]), parts[5])
                            
                            cardDirection = parts[3]
                            cardDirection2 = parts[5]
                        except ValueError:
                            pass
                elif parts[0] == '$GPRMC':
                    if len(parts) >= 10:
                        try:
                            # Had to read in from a different NMEA sentence because 
                            date = parts[9]
                            time = parts[1]
                        
                            formatted_date = "20{2}-{1}-{0}".format(date[:2], date[2:4], date[4:6])
                            formatted_time = "{0}:{1}:{2}".format(time[:2], time[2:4], time[4:6])
                        except ValueError:
                            pass

                closest_city = findCity(latitude, longitude, cities)
                closest_landmark = findLandmark(latitude, longitude, landmarks)
                
                # Opens txt file to check what the LCD should display
                with open("data.txt", "r") as file:
                    fileData = file.read(1)
                
                #If the 'z' flag is set send GPS data, else user data 
                if fileData == 'z':
                    await update_lcd_data(formatted_time, latitude, longitude, closest_city, closest_landmark, locFlag)
                else:
                    await update_lcd_data(formatted_time, latitude, longitude, closest_city, closest_landmark, fileData)
                
                
                print(locFlag)
        await asyncio.sleep_ms(1000)

"""
Function to update the LCD display based off of passed in data 
"""    
async def update_lcd_data(formatted_time, latitude, longitude, closest_city, closest_landmark, locFlag):
    lcd.clear()
    lcd.putstr("Time:")
    lcd.move_to(0, 1)
    lcd.putstr(str(formatted_time))
    await asyncio.sleep(2)

    # Conditional statement to display corresponding info based off of passed in flag
    if locFlag == 'a':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(40.71, -74.00))
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("City: NYC,USA")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark:Statue of Liberty,USA")
        await asyncio.sleep(2)
    elif locFlag == 'b':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(37.77, -122.41))
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("City:San Francisco,USA")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark:Golden Gate Bridge")
        await asyncio.sleep(2)
    elif locFlag == 'c':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(35.22, -97.43))
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("City: Norman, Oklahoma, USA")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark: OU")
        await asyncio.sleep(2)
    elif locFlag == 'd':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(34.05, -118.24))
        await asyncio.sleep(2)        

        lcd.clear()
        lcd.putstr("City:Los Angeles, USA")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark:Hollywood Sign")
        await asyncio.sleep(2)
    elif locFlag == 'e':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(41.87, -87.62))
        await asyncio.sleep(2)
    
        lcd.clear()
        lcd.putstr("City:Chicago, USA")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark:Millennium Park")
        await asyncio.sleep(2)
        
        
    elif locFlag == 'f':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(51.50, -0.12))
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("City:London, UK")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark:Big Ben")
        await asyncio.sleep(2)
    elif locFlag == 'g':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(35.68, 139.75))
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("City:Tokyo, Japan")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark:Tokyo Tower")
        await asyncio.sleep(2)
    elif locFlag == 'h':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(25.27, 55.29))
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("City:Dubai, United Arab Emirates")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark:Burj Khalifa")
        await asyncio.sleep(2)
    elif locFlag == 'i':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(48.85, 2.35))
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("City: Paris, France")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark: Eiffel Tower")
        await asyncio.sleep(2)
    elif locFlag == 'j':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(-33.86, 151.20))
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("City: Sydney, Australia")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark: Sydney Opera House")
        await asyncio.sleep(2)
    elif locFlag == 'k':
        lcd.clear()
        lcd.putstr("Coords:")
        lcd.move_to(0, 1)
        lcd.putstr("{}, {}".format(20.68, -88.56))
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("City: University of Oklahoma, USA")
        await asyncio.sleep(2)
        
        lcd.clear()
        lcd.putstr("Landmark: University Campus")
        await asyncio.sleep(2)

    lcd.clear()

        

""" 
Return the unique id of the device as a string 
"""
def uid():
    return "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
        *machine.unique_id())

MANUFACTURER_ID = const(0x02A29)
MODEL_NUMBER_ID = const(0x2A24)
SERIAL_NUMBER_ID = const(0x2A25)
HARDWARE_REVISION_ID = const(0x2A26)
BLE_VERSION_ID = const(0x2A28)

led = machine.Pin("LED", machine.Pin.OUT)

_ENV_SENSE_UUID = bluetooth.UUID(0x180A)
_GENERIC = bluetooth.UUID(0x1848)
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x1800)
_BUTTON_UUID = bluetooth.UUID(0x2A6E)

_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL = const(384)

# Advertising frequency
ADV_INTERVAL_MS = 250_000

device_info = aioble.Service(_ENV_SENSE_UUID)

connection = None

# Creates the characteristics for device info
aioble.Characteristic(device_info, bluetooth.UUID(MANUFACTURER_ID), read=True, initial="BasePi")
aioble.Characteristic(device_info, bluetooth.UUID(MODEL_NUMBER_ID), read=True, initial="1.0")
aioble.Characteristic(device_info, bluetooth.UUID(SERIAL_NUMBER_ID), read=True, initial=uid())
aioble.Characteristic(device_info, bluetooth.UUID(HARDWARE_REVISION_ID), read=True, initial=sys.version)
aioble.Characteristic(device_info, bluetooth.UUID(BLE_VERSION_ID), read=True, initial="1.0")

remote_service = aioble.Service(_GENERIC)

locationData = aioble.Characteristic(
    remote_service, _BUTTON_UUID, read=True, notify=True
)

aioble.register_services(remote_service, device_info)

connected = False

"""
Function to write and notify slave device of new command 
"""
async def sendFlag():    
    global locFlag
    
    while True:
        with open("data.txt", "r") as file:
            fileData = file.read(1)
        if not connected:
            await asyncio.sleep_ms(1000)
            continue
        if connected:
            if fileData == 'z':
                locationData.write(locFlag)
                locationData.notify(connection, locFlag)
            else:
                locationData.write(fileData)
                locationData.notify(connection, fileData) #Need this for control.py to sense
        await asyncio.sleep_ms(10)
            
"""
Function to show possible slave devices that it is available 
""" 
async def announce():
    global connected, connection
    while True:
        connected = False
        try:
            async with await aioble.advertise(
                ADV_INTERVAL_MS, 
                name="BasePi", 
                appearance=_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL, 
                services=[_ENV_SENSE_TEMP_UUID]
            ) as connection:
                connected = True
                
                while connected:
                    # You can add specific data handling or monitoring logic here
                    # For instance, await asyncio.sleep(1) to keep the task alive
                    
                    # If you don't have any specific handling here, use a sleep statement
                    await asyncio.sleep(1)
                    
        except aioble.BLEDisconnectError as e:
            connected = False
            # Attempt reconnection or handle disconnection gracefully
            while not connected:
                try:
                    async with await aioble.advertise(
                        ADV_INTERVAL_MS, 
                        name="BasePi", 
                        appearance=_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL, 
                        services=[_ENV_SENSE_TEMP_UUID]
                    ) as connection:
                        connected = True
                except aioble.BLEDisconnectError as e:
                    await asyncio.sleep(1)  # Add a delay before reconnection attempt
        await asyncio.sleep(1)  # Add a delay before retrying the connection

        
"""
Function to blink onboard LED to help debug 
"""
async def blink():
    toggle = True
    while True:
        led.value(toggle)
        toggle = not toggle
        blink = 1000
        if connected:
            blink = 1000
        else:
            blink = 250
        await asyncio.sleep_ms(blink)
        
"""
Main function to gather all functions that should be continually running 
"""
async def main():
    tasks = [
        asyncio.create_task(announce()),
        asyncio.create_task(blink()),
        asyncio.create_task(flag()),
        asyncio.create_task(sendFlag()),
        asyncio.create_task(getNMEA()),
    ]
    await asyncio.gather(*tasks) # Gathers the task 

asyncio.run(main()) # Runs the tasks 

