import aioble
import bluetooth
import machine
import uasyncio as asyncio

_REMOTE_UUID = bluetooth.UUID(0x1848)
_GENERIC = bluetooth.UUID(0x1800)
_REMOTE_CHARACTERISTICS_UUID = bluetooth.UUID(0x2A6E)

"""
led = machine.Pin("LED", machine.Pin.OUT)
led0 = machine.Pin(2, machine.Pin.OUT)
led0.value(False)
led1 = machine.Pin(3, machine.Pin.OUT)
led1.value(False)
led2 = machine.Pin(4, machine.Pin.OUT)
led2.value(False)
led3 = machine.Pin(5, machine.Pin.OUT)
led3.value(False)
led4 = machine.Pin(6, machine.Pin.OUT)
led4.value(False)
led5 = machine.Pin(7, machine.Pin.OUT)
led5.value(False)
led6 = machine.Pin(8, machine.Pin.OUT)
led6.value(False)
led7 = machine.Pin(9, machine.Pin.OUT)
led7.value(False)
led8 = machine.Pin(10, machine.Pin.OUT)
led8.value(False)
led9 = machine.Pin(11, machine.Pin.OUT)
led9.value(False)
led10 = machine.Pin(12, machine.Pin.OUT)
led10.value(False)
"""

led = machine.Pin("LED", machine.Pin.OUT)
# Initialize LED pins in a list
led_pins = [machine.Pin(2, machine.Pin.OUT),
            machine.Pin(3, machine.Pin.OUT),
            machine.Pin(4, machine.Pin.OUT),
            machine.Pin(5, machine.Pin.OUT),
            machine.Pin(6, machine.Pin.OUT),
            machine.Pin(7, machine.Pin.OUT),
            machine.Pin(8, machine.Pin.OUT),
            machine.Pin(9, machine.Pin.OUT),
            machine.Pin(10, machine.Pin.OUT),
            machine.Pin(11, machine.Pin.OUT),
            machine.Pin(12, machine.Pin.OUT)]

# Initially turn off all LEDs
for pin in led_pins:
    pin.value(False)

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
"""
def selectLocation(command):
    if command == b'a':
        led0.value(True)
        led1.value(False)
        led2.value(False)
        led3.value(False)
        led4.value(False)
        led5.value(False)
        led6.value(False)
        led7.value(False)
        led8.value(False)
        led9.value(False)
        led10.value(False)
    elif command == b'b':
        led0.value(False)
        led1.value(True)
        led2.value(False)
        led3.value(False)
        led4.value(False)
        led5.value(False)
        led6.value(False)
        led7.value(False)
        led8.value(False)
        led9.value(False)
        led10.value(False)
    elif command == b'c':
        led0.value(False)
        led1.value(False)
        led2.value(True)
        led3.value(False)
        led4.value(False)
        led5.value(False)
        led6.value(False)
        led7.value(False)
        led8.value(False)
        led9.value(False)
        led10.value(False)
    elif command == b'd':
        led0.value(False)
        led1.value(False)
        led2.value(False)
        led3.value(True)
        led4.value(False)
        led5.value(False)
        led6.value(False)
        led7.value(False)
        led8.value(False)
        led9.value(False)
        led10.value(False)
    elif command == b'e':
        led0.value(False)
        led1.value(False)
        led2.value(False)
        led3.value(False)
        led4.value(True)
        led5.value(False)
        led6.value(False)
        led7.value(False)
        led8.value(False)
        led9.value(False)
        led10.value(False)
    elif command == b'g':
        led0.value(False)
        led1.value(False)
        led2.value(False)
        led3.value(False)
        led4.value(False)
        led5.value(True)
        led6.value(False)
        led7.value(False)
        led8.value(False)
        led9.value(False)
        led10.value(False)
    elif command == b'h':
        led0.value(False)
        led1.value(False)
        led2.value(False)
        led3.value(False)
        led4.value(False)
        led5.value(False)
        led6.value(True)
        led7.value(False)
        led8.value(False)
        led9.value(False)
        led10.value(False)
    elif command == b'i':
        led0.value(False)
        led1.value(False)
        led2.value(False)
        led3.value(False)
        led4.value(False)
        led5.value(False)
        led6.value(False)
        led7.value(True)
        led8.value(False)
        led9.value(False)
        led10.value(False)
    elif command == b'j':
        led0.value(False)
        led1.value(False)
        led2.value(False)
        led3.value(False)
        led4.value(False)
        led5.value(False)
        led6.value(False)
        led7.value(False)
        led8.value(True)
        led9.value(False)
        led10.value(False)
    elif command == b'y':
        led0.value(False)
        led1.value(False)
        led2.value(False)
        led3.value(False)
        led4.value(False)
        led5.value(False)
        led6.value(False)
        led7.value(False)
        led8.value(False)
        led9.value(True)
        led10.value(False)
    elif command == b'f':
        led0.value(False)
        led1.value(False)
        led2.value(False)
        led3.value(False)
        led4.value(False)
        led5.value(False)
        led6.value(False)
        led7.value(False)
        led8.value(False)
        led9.value(False)
        led10.value(True)
    elif command == b'!':
        print("GPS Error")
    else:
        print("No GPS data found")
"""

def selectLocation(command):
    # Map commands to LED indices
    commands_to_led = {
        b'a': 0, b'b': 1, b'c': 2, b'd': 3, b'e': 4,
        b'g': 5, b'h': 6, b'i': 7, b'j': 8, b'y': 9,
        b'f': 10, b'!': -1  # Define the mapping of commands to LED indices
    }

    # Get the LED index from the command mapping
    led_index = commands_to_led.get(command)
    
    if led_index is not None and led_index != -1:
        # Turn off all LEDs
        for pin in led_pins:
            pin.value(False)
        
        # Turn on the corresponding LED
        led_pins[led_index].value(True)
    elif led_index == -1:
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
                


