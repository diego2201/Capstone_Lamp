import tkinter as tk
from tkinter import ttk
import math

# Imports the functions module 
import functionWrapper as functions

# Defines season colors
NORTH_COLORS = {
    "Spring": "green",
    "Summer": "yellow",
    "Autumn": "orange",
    "Winter": "white",
}

SOUTH_COLORS = {
    "Spring": "Autumn",
    "Summer": "Winter",
    "Autumn": "Spring",
    "Winter": "Summer",
}

# Creates the main window
root = tk.Tk()
root.title('EDL GUI')

# Creates a Notebook to manage separate tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Creates a tab for user input 
userTab = ttk.Frame(notebook)
notebook.add(userTab, text='User Input')

# Creates a tab for GPS data input
gpsDataTab = ttk.Frame(notebook)
notebook.add(gpsDataTab, text='GPS Data')

# Gets a list of the available options based off of defined dict in functions 
locationOptions = list(functions.imagePath.keys())

# Function to render a simple globe based on the selected season
"""
Function to render the globe based on the selected season 
"""
def drawGlobe(season):
    canvas.delete("globe")
    radius = 100
    centerX, centerY = 150, 150
    northHemi = radius
    southHemi = radius

    # Creates the northern hemisphere 
    canvas.create_arc(
        centerX - northHemi,
        centerY - northHemi,
        centerX + northHemi,
        centerY + northHemi,
        start=0,
        extent=180,
        outline="black",
        fill=NORTH_COLORS.get(season, "white"),
        tags="globe",
    )

    # Creates the southern hemisphere
    canvas.create_arc(
        centerX - southHemi,
        centerY - southHemi,
        centerX + southHemi,
        centerY + southHemi,
        start=0,
        extent=-180,
        outline="black",
        fill=NORTH_COLORS.get(SOUTH_COLORS.get(season), "white"),
        tags="globe",
    )

# GUI components for the user input tab
seasonPrompt = tk.Label(userTab, text='Select a Season:')
seasonPrompt.pack()
selectedSeason = tk.StringVar() # Stores the selected season 
seasonMenu = tk.OptionMenu(userTab, selectedSeason, *NORTH_COLORS.keys()) # Displays the option to user 
seasonMenu.pack()

# GUI component for the location input tab 
locationPrompt = tk.Label(userTab, text='Select a Major City:')
locationPrompt.pack()
selectedLocation = tk.StringVar()
locationMenu = tk.OptionMenu(userTab, selectedLocation, *locationOptions)
locationMenu.pack()

"""
Function to store all of the commands that should be run when the submit button is pressed 
"""
def imBtnCmds():
    drawGlobe(selectedSeason.get())
    functions.setFlag(selectedLocation.get(), 0)
    functions.openImage(selectedLocation.get(), result)

# Button to submit user input 
openImageBtn = tk.Button(
    userTab,
    text='Submit',
    command=imBtnCmds
)
openImageBtn.pack()
result = tk.Label(userTab, text='')
result.pack()
canvas = tk.Canvas(userTab, width=300, height=300)
canvas.pack()

"""
Function to store all of the commands that should be run when the submit button is pressed 
for the GPS
"""
def gpsBtnCmds():
    functions.getFlag()
    functions.setFlag(selectedLocation.get(), 1)
    functions.openImage(functions.readFile(), gpsResult)

gpsImageBtn = tk.Button(
    gpsDataTab,
    text='Get Location Data',
    command=gpsBtnCmds
)
gpsImageBtn.pack()
gpsResult = tk.Label(gpsDataTab, text='')
gpsResult.pack()

"""
Function to store all of the commands that should be run for pres mode 
"""
def presCmd():
    functions.setFlag("Devon", 0)
    functions.openImage("Devon", presResult)

presBtn = tk.Button(
    root, 
    text="Presentation",
    command=presCmd
)
presBtn.pack()
presResult = tk.Label(root, text='')
presResult.pack()

"""
Function to store all of the commands that should be run to exit application
"""
def exit():
    functions.setFlag(selectedLocation.get(), 1)
    root.destroy()

# Creates the button to exit the application
exitBtn = tk.Button(
    root, 
    text="Exit Application", 
    command=exit
)
exitBtn.pack(side="bottom", pady=10)

# Runs the GUI main loop
root.mainloop()