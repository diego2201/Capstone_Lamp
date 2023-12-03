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
    data = serial_connection.read(129)
    if data == b"EOF":
        break
    print(data)
    deskFile.seek(0)
    deskFile.write(data)
    
    time.sleep(10)
    

# Close the files and serial connection
filePath.close()
serial_connection.close()
