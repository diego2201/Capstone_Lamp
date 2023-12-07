import aioble
import bluetooth
import machine
import uasyncio as asyncio

_REMOTE_UUID = bluetooth.UUID(0x1848)
_GENERIC = bluetooth.UUID(0x1800)
_REMOTE_CHARACTERISTICS_UUID = bluetooth.UUID(0x2A6E)

led = machine.Pin("LED", machine.Pin.OUT)
led0 = machine.Pin(2, machine.Pin.OUT)
connected = False
alive = False

"""
Function to scan available bt devices and connect to specified device name
"""
async def findBase():
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            #Searchs for "BasePi"
            if result.name() == "BasePi": 
                print("Found BasePi") #Debug statement
                for item in result.services():
                    print(item)
                if _GENERIC in result.services():
                    print("Found Remote Service") #Debug statement
                    return result.device
    return None

"""
Function to blink onboard LED for debugging 
"""
async def blink():
    print('blink task started') #Debug statement
    toggle = True
    while True:
        blink = 250
        led.value(toggle)
        toggle = not toggle
        if connected:
            blink = 1000
        else:
            blink = 250
        await asyncio.sleep_ms(blink)
    print('blink task stopped') #Debug statement

"""
Function to turn on corresponding LED based off of read in 
location flag from master device 
"""
def selectLocation(command):
    if command == b'a':
        print("New York City, USA")      
    elif command == b'b':
        print("San Francisco, USA")
        led0.value(1)
    elif command == b'c':
        print("Norman, Oklahoma, USA")
        led0.value(0)
    elif command == b'd':
        print("Los Angeles, USA")
    elif command == b'e':
        print("Chicago, USA")
    elif command == b'f':
        print("Tokyo, Japan")
    elif command == b'h':
        print("Dubai, United Arab Emirates")
    elif command == b'i':
        print("Paris, France")
    elif command == b'j':
        print("Sydney, Australia")
    elif command == b'y':
        print("Devon Energy Hall")
    elif command == b'!':
        print("GPS Error")
    else:
        print("No GPS data found")

"""
Function with error handling for failed connections, disconnections,
no matching device name, etc.
If connected, begins to read in data and calls selectedLocation() function.
"""
async def communicate():
    print("peripheral task started")  # Debug statement

    global connected, alive
    connected = False

    # Find a remote device
    device = await findBase()

    if not device:
        print("No remote found")
        return

    try:
        print("connecting to", device)
        connection = await device.connect()

    except asyncio.TimeoutError:
        print("Timeout during connection")
        return

    async with connection:
        print("connected")  # Debug statement
        alive = True
        connected = True

        # Discover and access the robot service and its characteristic
        robot_service = await connection.service(_REMOTE_UUID)
        control_characteristic = await robot_service.characteristic(_REMOTE_CHARACTERISTICS_UUID)

        while True:
            try:
                # Check for remote disconnection
                if robot_service is None:
                    print("remote disconnected")  # Debug statement
                    alive = False
                    break

            except asyncio.TimeoutError:
                print("Timeout during discovery / service / characteristic")  # Debug statement
                alive = False
                break

            if control_characteristic is None:
                print("no control")
                alive = False
                break

            try:
                # Read data from the control characteristic
                data = await control_characteristic.read(timeout_ms=1000)

                # Subscribe to notifications for continuous data reception
                await control_characteristic.subscribe(notify=True)

                while True:
                    # Receive notified data and call selectLocation() function
                    command = await control_characteristic.notified()
                    selectLocation(command)
                    # print(command)  # Debug statement

            except Exception as e:
                print(f"something went wrong: {e}")  # Debug statement
                connected = False
                alive = False
                break

        # Close the connection when done
        await connection.disconnected()
        print("disconnected")  # Debug statement
        alive = False

"""
Main function to gather all needed tasks 
"""
async def main():
    tasks = []
    tasks = [
        asyncio.create_task(blink()),
        asyncio.create_task(communicate()),
    ]
    await asyncio.gather(*tasks)

#Runs all the tasks 
while True:
    asyncio.run(main())
                
