import tkinter as tk
from tkinter import ttk
import math

# Import the functions module
import functionWrapper as functions

# Define season colors
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

# Create the main window
root = tk.Tk()
root.title('EDL GUI')

# Create a Notebook to manage tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create a tab for the Season and Location selector
userTab = ttk.Frame(notebook)
notebook.add(userTab, text='User Input')

# Create a tab for the GPS data
gpsDataTab = ttk.Frame(notebook)
notebook.add(gpsDataTab, text='GPS Data')

# Common components for both tabs
locationOptions = list(functions.imagePath.keys())

# Function to render a simple globe based on the selected season
def drawGlobe(season):
    canvas.delete("globe")
    radius = 100
    centerX, centerY = 150, 150
    northHemi = radius
    southHemi = radius

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

# UI components for the Season and Location tab
seasonPrompt = tk.Label(userTab, text='Select a Season:')
seasonPrompt.pack()
selectedSeason = tk.StringVar()
seasonMenu = tk.OptionMenu(userTab, selectedSeason, *NORTH_COLORS.keys())
seasonMenu.pack()

locationPrompt = tk.Label(userTab, text='Select a Major City:')
locationPrompt.pack()
selectedLocation = tk.StringVar()
locationMenu = tk.OptionMenu(userTab, selectedLocation, *locationOptions)
locationMenu.pack()

def imBtnCmds():
    drawGlobe(selectedSeason.get())
    functions.setFlag(selectedLocation.get(), 0)
    functions.openImage(selectedLocation.get(), result)

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

def exit():
    functions.setFlag(selectedLocation.get(), 1)
    root.destroy()

# Create the button to exit the application
exitBtn = tk.Button(
    root, 
    text="Exit Application", 
    command=exit
)
exitBtn.pack(side="bottom", pady=10)

# Run the Tkinter main loop
root.mainloop()