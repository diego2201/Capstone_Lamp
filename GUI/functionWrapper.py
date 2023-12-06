import subprocess
import serial
import time 

inputFile = "/home/capstone/Desktop/Capstone_Lamp/GUI/input.txt"
outputFile = "/home/capstone/Desktop/Capstone_Lamp/GUI/output.txt"

locationFlag = ''

# Define a dictionary of major cities/locations and their image paths
imagePath = {
    "New York City, USA": '/home/capstone/Desktop/Capstone_Lamp/GUI/Images/NYC.jpeg',
    "San Francisco, USA": '/home/capstone/Desktop/Capstone_Lamp/GUI/Images/SanFran.jpeg',
    "Norman, Oklahoma, USA": '/home/capstone/Desktop/Capstone_Lamp/GUI/Images/OU.jpeg',
    "Los Angeles, USA": '/home/capstone/Desktop/Capstone_Lamp/GUI/Images/LA.jpeg',
    "Chicago, USA": '/home/capstone/Desktop/Capstone_Lamp/GUI/Images/Chicago.jpeg',    
    "London, United Kingdom": '/home/capstone/Desktop/Capstone_Lamp/GUI/Images/London.jpeg',
    "Tokyo, Japan": '/home/capstone/Desktop/Capstone_Lamp/GUI/Images/Tokyo.jpeg',
    "Dubai, United Arab Emirates": '/home/capstone/Desktop/Capstone_Lamp/GUI/Images/Dubai.jpeg',
    "Paris, France": '/home/capstone/Desktop/Capstone_Lamp/GUI/Images/Pari.jpeg',
    "Sydney, Australia": '/home/capstone/Desktop/Capstone_Lamp/GUI/Images/Syn.jpeg'
}

locationDict = {
    'a': "New York City, USA",
    'b': "San Francisco, USA",
    'c': "Norman, Oklahoma, USA",
    'd': "Los Angeles, USA",
    'e': "Chicago, USA",
    'f': "London, United Kingdom",
    'g': "Tokyo, Japan",
    'h': "Dubai, United Arab Emirates",
    'i': "Paris, France",
    'j': "Sydney, Australia",
    'k': 'University of Oklhoma, USA',
    '!': 'GPS Error',
    'z': 'z'
}

def getKey(target):
    for key, value in locationDict.items():
        if value == target:
            return key
    return None

# Function to open an image based on the selected location
def openImage(location, result):
    
    # Get the image path for the selected location
    path = imagePath.get(location)

    # Display the result label
    if path:
        # Open the image in the terminal (change the command as needed)
        subprocess.run(['open', path])
    else:
        result.config(text='Image not found.')

def readFile():
    with open(inputFile, 'rb') as file:
        data = file.read().decode('utf-8', errors='ignore')

    parsedData = ''.join(char for char in data if char.isprintable())
    print(locationDict.get(parsedData))
    # writeFile('#', 1)

    return locationDict.get(parsedData)

# def writeFile(data, clear):
#     if clear == 0:
#         print(data)
#         print(getKey(data))
        
#         with open(outputFile, "w") as file:
#             file.seek(0)
#             file.write(getKey(data))
#     elif clear == 1:
#         with open(outputFile, "w") as file:
#             file.seek(0)
#             file.write((data))

def getFlag():
    global locationFlag

    # writeFile('#', 1)
    # Configure the serial connection
    port = "/dev/ttyACM0" 
    baudrate = 115200
    serialCon = serial.Serial(port, baudrate)

    # Open a file on your computer to write the received data
    deskFile = open(inputFile, "wb")

    # Read and write data until the transfer is complete
    data = serialCon.read(3)
    locationFlag = serialCon.read(1)
    print("locflag:", data)
    deskFile.seek(0) #Overwrite the loction flag
    deskFile.write(data)

    # Close the files and serial connection
    deskFile.close()
    serialCon.close()

def setFlag(loc, clear):
    port = "/dev/ttyACM0"
    baudrate = 115200
    serialCon = serial.Serial(port, baudrate)

    if clear == 0:
        flag = getKey(loc)
        print(flag)
        serialCon.write((flag + ',').encode())

        serialCon.close()
        time.sleep(1)
        serialCon.close()
    elif clear == 1:
        serialCon.write((locationDict.get('z') + ',').encode())
        serialCon.close()
        time.sleep(1)
        serialCon.close()    
