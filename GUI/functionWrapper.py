import subprocess

# Define a dictionary of major cities/locations and their image paths
image_paths = {
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

# Function to open an image based on the selected location
def open_image(selected_location, result_label):
    
    # Get the image path for the selected location
    image_path = image_paths.get(selected_location)

    # Display the result label
    if image_path:
        # Open the image in the terminal (change the command as needed)
        subprocess.run(['open', image_path])
    else:
        result_label.config(text='Image not found.')

def read_gps_data(file_path):
    gps_data = {}  # Initialize an empty dictionary to store the data

    try:
        with open(file_path, 'r') as file:
            current_key = None
            for line in file:
                line = line.strip()
                if line:
                    if line.startswith("Latitude: "):
                        current_key = "Latitude"
                        gps_data[current_key] = float(line.split(": ")[1])

                    elif line.startswith("Longitude: "):
                        current_key = "Longitude"
                        gps_data[current_key] = float(line.split(": ")[1])

                    elif line.startswith("Date: "):
                        current_key = "Date"
                        gps_data[current_key] = line.split(": ")[1]

                    elif line.startswith("Time: "):
                        current_key = "Time"
                        gps_data[current_key] = line.split(": ")[1]

                    elif line.startswith("Closest City: "):
                        current_key = "Closest City"
                        gps_data[current_key] = line.split(": ")[1]

                    elif line.startswith("Closest Landmark: "):
                        current_key = "Closest Landmark"
                        gps_data[current_key] = line.split(": ")[1]

                    else:
                        # If the line doesn't match any known format, continue with the current key
                        if current_key:
                            gps_data[current_key] += " " + line

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")

    return gps_data

def readFile(filePath):
    gps_data = {}  # Initialize an empty dictionary to store the data
    locationFlag = ''
    file = open(filePath, 'r')
    char = ''
    while 1:
        
        # read by character
        char = file.read(1)          
        if not char: 
            break
            
        print(char)
    
        
    file.close()
    return char

# def display_gps_data(gps_data, result_label):
#     result_text = "GPS Data:\n" + "\n".join([f"{key}: {value}" for key, value in gps_data.items()])
#     result_label.config(text=result_text)

def display_gps_data(gps_data):
    result_text = gps_data
