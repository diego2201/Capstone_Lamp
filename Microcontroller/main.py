import machine
import utime
import math
from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd

# Defines I2C pins and freq
i2c = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

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

closest_city = None
closest_landmark = None

test1 = 0.0
test2 = 0.0

# Defines a list of major cities and their coords (latitude, longitude)
cities = {
    "New York City, USA": (40.7128, -74.0060),
    "San Francisco, USA": (37.7749, -122.4194),
    "Norman, USA": (35.2220, -97.4395),
    "Los Angeles, USA": (34.0522, -118.2437),
    "Chicago, USA": (41.8781, -87.6298),
    "Beijing, China": (39.9042, 116.4074),
    "Shanghai, China": (31.2304, 121.4737),
    "London, United Kingdom": (51.5074, -0.1278),
    "Tokyo, Japan": (35.682839, 139.759455),
    "São Paulo, Brazil": (-23.5505, -46.6333),
    "Istanbul, Turkey": (41.0082, 28.9784),
    "Dubai, United Arab Emirates": (25.276987, 55.296249),
    "Singapore, Singapore": (1.3521, 103.8198),
    "Mexico City, Mexico": (19.4326, -99.1332),
    "Paris, France": (48.8566, 2.3522),
    "Sydney, Australia": (-33.8651, 151.2099)
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
    closest_city = None
    closest_distance = float("inf")

    for city, coordinates in cities.items():
        distance = calculate_distance((latitude, longitude), coordinates)
        if distance < closest_distance:
            closest_city = city
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

# Specify the location and filename for the new file
# Saves directly to Raspberry Pi
file_path = "output.txt"

# Opens the file for writing 
output_file = open(file_path, "w")

# Main loop to read and parse NMEA sentences
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
                        test1 = float(parts[2])
                        test2 = float(parts[4])
                        
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

            output_file.write("Latitude: {0:.6f}\n".format(latitude))
            output_file.write("Longitude: {0:.6f}\n".format(longitude))
            output_file.write("Date: {0}\n".format(formatted_date))
            output_file.write("Time: {0}\n".format(formatted_time))
            output_file.write("Closest City: {0}\n".format(closest_city))
            output_file.write("Closest Landmark: {0}\n".format(closest_landmark))
            output_file.write("\n")

            print("Latitude: {0:.6f}".format(latitude))
            print("Longitude: {0:.6f}".format(longitude))
            
            print("Test1: {0:.6f}".format(test1))
            print("Test2: {0:.6f}".format(test2))
            
            print("Date: {}".format(formatted_date))
            print("Time: {}".format(formatted_time))
            print("Closest City: {}".format(closest_city))
            print("Closest Landmark: {}".format(closest_landmark))
            print("Cardinal Direction: {}".format(cardDirection))
            print("Cardinal Direction: {}".format(cardDirection2))

            print("")
            
            
        lcd.putstr("Time:"+str(formatted_time))
        sleep(2)
        lcd.clear()
        lcd.putstr("Latitude:" + "\n" + str(latitude))
        sleep(2)
        lcd.clear()
        lcd.putstr("Longitude:" + "\n" + str(longitude))
        sleep(2)
        lcd.clear()
        lcd.putstr("City:"+str(closest_city))
        sleep(2)
        lcd.clear()
        lcd.putstr("Landmark:"+str(closest_landmark))
        sleep(2)
        lcd.clear()

    utime.sleep(1)
    
# Closes the output file
output_file.close()