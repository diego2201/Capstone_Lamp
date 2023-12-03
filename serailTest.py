import serial
import os
import time

# Configure the serial connection
port = "/dev/ttyACM0" 
baudrate = 115200
serial_connection = serial.Serial(port, baudrate)

filePath = "/home/capstone/Desktop/test.txt"

# Open a file on your computer to write the received data
deskFile = open(filePath, "wb")

# Read and write data until the transfer is complete
while True:
    #129 bits for full data, 5 for just location flag
    
    data = serial_connection.read(3)
    if data == b"EOF":
        break
    print(data)
    deskFile.seek(0) #Overwrite the loction flag
    deskFile.write(data)
    
    time.sleep(2)
    

# Close the files and serial connection
filePath.close()
serial_connection.close()
