# Spiers NT Capstone Project - Fall 2023
The project is to design a spherical globe lamp that accurately depicts the interaction between the planet Earth and the Sun. The lamp should provide enough light to reasonably illuminate one engineer's desk, and creatively indicate the position of the lamp itself in relation to major countries, cities, and landmarks. The globe will need to rotate in two directions to accurately simulate the motion of the Earth and I would like the light source (Sun) to remain fixed such that the dateline illustrating the rising and the setting of the Sun is the primary light output of the lamp. The lamp is not allowed to connect to the internet and it must be powered by a standard 110VAC receptacle (no batteries).

## Software Environment 
<strong>OS</strong>: The GUI should be running on Raspberry Pi OS (Legacy), being a port of Debian Bullseye. After testing the GUI will not work with other more recent versions of Raspberry Pi OS. 
    In switching to this OS version you lose very minimial functionalities, such as being able to set the icon of the ".desktop" file. <br /> <br />

In order to setup the software environment we will need to run a few terminal commands. The following is to get the touchscreen working 
```
git clone https://github.com/waveshare/LCD-show.git
cd LCD-show/
chmod +x LCD35-show
./LCD35-show
```
This will restart your device. You should now see the OS displayed on the touchscreen. <br />
You may also run into the case where you cannot run the GUI from the start up script `GUI.desktop'. Becuase of this you may need to run the folllowing commands. 
```
cd /usr/bin
sudo cp lxterminal xterm
```

<strong>Raspberry Pi Pico</strong>: These Picos both interally maintain their respective and correct versions of the code. What does that mean? Essentially that there is no need to worry about the version of the code for these two. What we do have to watch out for is the defined "PORT" string for the master Pi Pico. We need to assure that the assigned string for this port is "/dev/ttyACM0". In order to check this we can simply open up a new Thonney window and check the bottom right of the screen. However, there may be the chance where that is not the case. The SBC may assign the port to "/dev/ttyACM1", in this instance we can simply unplug the master pico, wait a few seconds, then plug back in. <br />

# Code Explanation 
## GUI 
Within the GUI folder there are two main python scripts, "main.py" and "functionWrapper.py". <br />
For the purposes of this project we use a few imports: <br />
* tkinter
* math
* subprocess
* serial
* time 
These two imports are incldued with the standard python libaruy installation available with the Raspberry Pi OS. <br />
The main script creates and hosts the GUI components, while calling the functions from functionWrapper to implement any logic (such as serial connections, file reading, etc.). 
The functionWrapper script hosts the actually functionality of the project. Here we creates functions to perfom vaious necessary logic needed to complete this project. For example file reading, establishing a serial connection with the master pico to read or set the location flag, and more. <br />

<strong>main.py</strong>
* `openImageBtn()` This method collects all of the necessary functions that should be ran when the user presses the button to display information based off of their own input
* `gpsBtnCmd()` This method collects all of the necessary functions that should be ran when the user presses the button to display information based off of the GPS input  
* `presCmd()` This method collects all of the necessary functions that should be ran when the user presses the button to display the presentation location information (Devon) 
* `exit()` This method collects all of the necessary functions that should be ran when the user presses the button exit the application

<strong>functionWrapper.py</strong>
* `getKey(target)` Since python does not have a built in function to get the key for a dictionary based off of the value I implemented this function to do just that 
* `openImage(location, result)` This function opens up the specified image as passed in by the main function (location). The result passed in is a tkinter object, this will display an error message if the image is not found, or unable to open  
* `readFile()` This function reads in the location flag located in the specified txt file. This flag will determine what is displayed to the user 
* `getFlag()` This function establishes a serial connection with the Pi Pico. The code in the pi pico prints out a statement, this print statement is then caught by the serial connection and is then stored into the specified txt file 
* `setFlag()` This function establishes a serial connection with the Pi Pico. This code sends a char over the serial communication. The code in the pi pico reads this bit in and then stores it into the specified file 

## Microcontroller 
Within the Microcontroller folder we contain all of the necessary files needed to run both of the Pi Picos. Since we are using a bluetooth connection we needed to implement two very important scripts one for the master pico and one for the slave (remote and control respectively). <br />
For the purposes of this project we use a few imports: <br />
* sys
* aioble
* bluetooth
* machine
* uasyncio 
* micropython 
* utime
* math
* time 
* uselect
All of these imports are supported by the micropython installation downloaded to both of the Pi Pico's. 

<strong>master.py</strong>
* `saveFile(data)` Function to write data to defined file 
* `flag()` function to read in a char from a serial connection, and then stores into specified file by calling saveFile()
* `calcDist(coord1, coord2)` Function to calculate distance between sets of coordinates using the Haversine formula
* `findCity(latitude, longitude, cities)` Function to find the nearest city based off of the distance calculates using calcDist()
* `findLandmark(latitude, longitude, landmarks)` Function to find the nearest landmark based off of the distance calculates using calcDist()
* `convertCoords(coord, direction)` Function to properly convert the coords read in from the NMEA sentence to the standard formatting 
* `getNMEA()` Function to establish connection to GPS receiver and constantly read in data in the form of a NMEA sentence. Then parses this sentence and stores to the appropriate variable, calling the respective functions to help collect accurate information 
* `uid()` Function to create a unique string id for the master pico
* `sendFlag()` Function to send flag over bluetooth to slave 
* `announce()` Function to advertise that this device is in pairing mode and waiting to establish a connection
* `blink()` Function to blink the onboard LED to help ease troubleshooting. Fast blinks means that it has not been connected to anything else, slow blinks means that it has established a connection
* `main()` Gathers all of the async functions, stores them into a list and then runs them continually

<strong>slave.py</strong>
* `findBase()` Continually scans for all bluetooth devices available near by. Checks to see if it matches the preset name, if it does we establisha connection to this device 
* `blink()` Function to blink the onboard LED to help ease troubleshooting. Fast blinks means that it has not been connected to anything else, slow blinks means that it has established a connection
* `selectLocation()` Contains various conditional statements. Turns on the respective LED based off of what flag has been read in from the master device 
* `communicate()` Function that contains a lot of the logic to handle any errors with bluetooth connection. Such as any errors with disconnections, no connections, etc. Also receives data from the master once a connection has been made 
* `main()` Gathers all of the async functions, stores them into a list and then runs them continually

# Reference
* <strong>Bluetility</strong> used to help see low power Bluetooth devices : https://github.com/jnross/Bluetility <br />
* <strong>LCD Touchscreen</strong> Set up touchscreen for Raspberry Pi 4: https://core-electronics.com.au/guides/small-screens-raspberry-pi/ <br />
* <strong>Fix Script Error</strong> Used to help fix error, "Failed to execute child process "xterm"": https://raspberrypi.stackexchange.com/questions/91428/failed-to-execute-child-process-xterm<br />
