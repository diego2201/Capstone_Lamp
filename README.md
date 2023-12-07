# Spiers NT Capstone Project - Fall 2023
The project is to design a spherical globe lamp that accurately depicts the interaction between the planet Earth and the Sun. The lamp should provide enough light to reasonably illuminate one engineer's desk, and creaƟvely indicate the posiƟon of the lamp itself in relaƟon to major countries, cities, and landmarks. The globe will need to rotate in two directions to accurately simulate the motion of the Earth and I would like the light source (Sun) to remain fixed such that the dateline illustrating the rising and the setting of the Sun is the primary light output of the lamp. The lamp is not allowed to connect to the internet and it must be powered by a standard 110VAC receptacle (no batteries).

## Software Environment 
OS: The GUI should be running on Raspberry Pi OS (Legacy), being a port of Debian Bullseye. After testing the GUI will not work with other more recent versions of Raspberry Pi OS. 
    In switching to this OS version you lose very minimial functionalities, such as being able to set the icon of the ".desktop" file. </n>
Raspberry Pi Pico: These Picos both interally maintain their respective and correct versions of the code. What does that mean? Essentially that there is no need to worry about the version of the code for these two. What we do have to watch out for is the defined "PORT" string for the master Pi Pico. We need to assure that the assigned string for this port is "/dev/ttyACM0". In order to check this we can simply open up a new Thonney window and check the bottom right of the screen. However, there may be the chance where that is not the case. The SBC may assign the port to "/dev/ttyACM1", in this instance we can simply unplug the master pico, wait a few seconds, then plug back in. </n>

# Code Explanation 
## GUI 
Within the GUI folder there are two main python scripts, "main.py" and "functionWrapper.py".
The main script creates and hosts the GUI components, while calling the functions from functionWrapper to implement any logic (such as serial connections, file reading, etc.). 
The functionWrapper script hosts the actually functionality of the project. Here we creates functions to perfom vaious necessary logic needed to complete this project. For example file reading, establishing a serial connection with the master pico to read or set the location flag, and more 

## Microcontroller 
Within the Microcontroller folder we contain all of the necessary files needed to run both of the Pi Picos. Since we are using a bluetooth connection we needed to implement two very important scripts one for the master pico and one for the slave (remote and control respectively). 

##

## Bluetooth
https://github.com/jnross/Bluetility </n>
-To help see the low power Bluetooth devices 