import sys

import aioble
import bluetooth
import machine
import uasyncio as asyncio
from micropython import const

import utime
import math
from time import sleep

# Defines UART pins and baud rate
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

# Define variables where we will store our NMEA data
latitude = 0.0
longitude = 0.0
date = ""
time = ""
formatted_date = ""
formatted_time = ""

cardDirection = ""
cardDirection2 = ""
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
    "Tokyo, Japan": (35.682839, 139.759455, 'f'),
    "Dubai, United Arab Emirates": (25.276987, 55.296249, 'h'),
    "Paris, France": (48.8566, 2.3522, 'i'),
    "Sydney, Australia": (-33.8651, 151.2099, 'j'),
    "University of Oklahoma, USA": (20.6843, -88.5678, 'k'),
}

# Defines a list of major landmarks and their coords (latitude, longitude)
landmarks = {
    "Statue of Liberty, USA": (40.6892, -74.0445),
    "Golden Gate Bridge, USA": (37.8199, -122.4783),
    "Great Wall of China, China": (40.4319, 116.5704),
    "Eiffel Tower, France": (48.858844, 2.294351),
    "Big Ben, United Kingdom": (51.5007, -0.1246),
    "Tokyo Tower, Japan": (35.6586, 139.7454),
    "Christ the Redeemer, Brazil": (-22.9519, -43.2106),
    "Hagia Sophia, Turkey": (41.0082, 28.9784),
    "Burj Khalifa, United Arab Emirates": (25.276987, 55.296249),
    "Marina Bay Sands, Singapore": (1.2835, 103.8595),
    "Pyramids of Giza, Egypt": (29.9792, 31.1344),
    "Sydney Opera House, Australia": (-33.8568, 151.2153),
    "Taj Mahal, India": (27.1751, 78.0421),
    "Petronas Twin Towers, Malaysia": (3.1588, 101.7141),
    "Cristo Redentor, Portugal": (32.9225, -16.7721),
    "University of Oklahoma, USA": (20.6843, -88.5678)
}

# Function to calculate the distance between two sets of coordinates using Haversine formula
def calculate_distance(coord1, coord2):
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

# Function to find the closest city
def find_closest_city(latitude, longitude, cities):
    global locFlag
    
    closest_city = None
    closest_distance = float("inf")

    for city, coordinates in cities.items():
        city_latitude, city_longitude, flag = coordinates  # Unpack the coordinates including the flag
        distance = calculate_distance((latitude, longitude), (city_latitude, city_longitude))
        if distance < closest_distance:
            closest_city = city
            locFlag = flag
            closest_distance = distance

    return closest_city


# Function to find the closest landmark
def find_closest_landmark(latitude, longitude, landmarks):
    closest_landmark = None
    closest_distance_landmark = float("inf")

    for landmark, coordinates in landmarks.items():
        distance = calculate_distance((latitude, longitude), coordinates)
        if distance < closest_distance_landmark:
            closest_landmark = landmark
            closest_distance_landmark = distance

    return closest_landmark

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

async def handle_gps_data():
    print('test')
    global latitude, longitude, formatted_date, formatted_time, cardDirection, cardDirection2, closest_city, closest_landmark
    
    # Define your GPS data processing logic here
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
                parts = data.split(',')

                if parts[0] == '$GPGGA':
                    if len(parts) >= 10:
                        try:     
                            latitude = convertCoords(float(parts[2]), parts[3])
                            longitude = convertCoords(float(parts[4]), parts[5])
                            
                            cardDirection = parts[3]
                            cardDirection2 = parts[5]
                        except ValueError:
                            pass
                elif parts[0] == '$GPRMC':
                    if len(parts) >= 10:
                        try:
                            date = parts[9]
                            time = parts[1]

                            formatted_date = "20{2}-{1}-{0}".format(date[:2], date[2:4], date[4:6])
                            formatted_time = "{0}:{1}:{2}".format(time[:2], time[2:4], time[4:6])
                        except ValueError:
                            pass

                closest_city = find_closest_city(latitude, longitude, cities)
                closest_landmark = find_closest_landmark(latitude, longitude, landmarks)

                print("Latitude: {0:.6f}".format(latitude))
                print("Longitude: {0:.6f}".format(longitude))
                print("City Flag: {}".format(locFlag))
                print("Date: {}".format(formatted_date))
                print("Time: {}".format(formatted_time))
                print("Closest City: {}".format(closest_city))
                print("Closest Landmark: {}".format(closest_landmark))
                print("Cardinal Direction: {}".format(cardDirection))
                print("Cardinal Direction: {}".format(cardDirection2))
                print("")
        await asyncio.sleep_ms(1000)

def uid():
    """ Return the unique id of the device as a string """
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

# Create characteristics for device info
aioble.Characteristic(device_info, bluetooth.UUID(MANUFACTURER_ID), read=True, initial="BasePi")
aioble.Characteristic(device_info, bluetooth.UUID(MODEL_NUMBER_ID), read=True, initial="1.0")
aioble.Characteristic(device_info, bluetooth.UUID(SERIAL_NUMBER_ID), read=True, initial=uid())
aioble.Characteristic(device_info, bluetooth.UUID(HARDWARE_REVISION_ID), read=True, initial=sys.version)
aioble.Characteristic(device_info, bluetooth.UUID(BLE_VERSION_ID), read=True, initial="1.0")

remote_service = aioble.Service(_GENERIC)

locationData = aioble.Characteristic(
    remote_service, _BUTTON_UUID, read=True, notify=True
)

print('registering services')
aioble.register_services(remote_service, device_info)

connected = False

async def remote_task():
    """ Send the event to the connected device """
    
    global formatted_time, closest_city, locFlag

    while True:
        if not connected:
            print('not connected')
            await asyncio.sleep_ms(1000)
            continue
        if connected:
            #print(f"BT connected: {connection}")
            locationData.write(locFlag)
            locationData.notify(connection, locFlag)
        else:
            print('connected')
        await asyncio.sleep_ms(10)
            
# Serially wait for connections. Don't advertise while a central is
# connected.    
async def peripheral_task():
    print('peripheral task started')
    global connected, connection
    while True:
        connected = False
        async with await aioble.advertise(
            ADV_INTERVAL_MS, 
            name="BasePi", 
            appearance=_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL, 
            services=[_ENV_SENSE_TEMP_UUID]
        ) as connection:
            print("Connection from", connection.device)
            connected = True
            print(f"connected: {connected}")
            await connection.disconnected()
            print(f'disconnected')
        

async def blink_task():
    print('blink task started')
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
        
async def main():
    tasks = [
        asyncio.create_task(peripheral_task()),
        asyncio.create_task(blink_task()),
        asyncio.create_task(remote_task()),
        asyncio.create_task(handle_gps_data()),
    ]
    await asyncio.gather(*tasks)

asyncio.run(main())

