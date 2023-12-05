import subprocess

# Define a dictionary of major cities/locations and their image paths
imagePath = {
    "New York City, USA": 'Images/NYC.jpeg',
    "San Francisco, USA": 'Images/SanFran.jpeg',
    "Norman, Oklahoma, USA": 'Images/OU.jpeg',
    "Los Angeles, USA": 'Images/LA.jpeg',
    "Chicago, USA": 'Images/Chicago.jpeg',
        
    "Beijing, China": 'Images/Bei.jpeg',
    "Shanghai, China": 'Images/Sha.jpeg',
        
    "London, United Kingdom": 'Images/London.jpeg',
    "Tokyo, Japan": 'Images/Tokyo.jpeg',
    "São Paulo, Brazil": 'Images/Sao.jpeg',
    "Istanbul, Turkey": 'Images/Istan.jpeg',
    "Dubai, United Arab Emirates": 'Images/Dubai.jpeg',
    "Singapore, Singapore": 'Images/Sing.jpeg',
    "Mexico City, Mexico": 'Images/MX.jpeg',
    "Paris, France": 'Images/Pari.jpeg',
    "Sydney, Australia": 'Images/Syn.jpeg'
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
    '!': 'GPS Error'
}

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

def readFile(filePath):
    with open(filePath, 'rb') as file:
        data = file.read().decode('utf-8', errors='ignore')
        # Get the string corresponding to the character from the dictionary
    parsedData = ''.join(char for char in data if char.isprintable())
    print(locationDict.get(parsedData))
    return locationDict.get(parsedData)

