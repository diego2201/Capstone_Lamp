import tkinter as tk
from tkinter import ttk
import math

# Import the functions module
import functionWrapper as functions

# Define season colors
SEASON_COLORS = {
    "Spring": "green",
    "Summer": "yellow",
    "Autumn": "orange",
    "Winter": "white",
}

OPPOSITE_SEASON = {
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
seasonLocationTab = ttk.Frame(notebook)
notebook.add(seasonLocationTab, text='User Input')

# Create a tab for the GPS data
gpsDataTab = ttk.Frame(notebook)
notebook.add(gpsDataTab, text='GPS Data')

# Common components for both tabs
location_choices = list(functions.image_paths.keys())

# Function to animate the Date Line
def animate_date_line(angle, increment):
    #canvas.delete("date_line")
    draw_date_line(angle)
    angle += math.radians(increment)
    if angle >= 360:
        angle = 180  # Reset the angle to restart the animation
    #canvas.after(10, animate_date_line, angle, increment)

# Function to draw the Date Line
def draw_date_line(angle):
    radius = 100
    center_x, center_y = 150, 150
    start_x = center_x + radius * math.cos(angle)
    start_y = center_y + radius * math.sin(angle)
    end_x = center_x + radius * math.cos(-angle)
    end_y = center_y + radius * math.sin(-angle)
    canvas.create_line(start_x, start_y, end_x, end_y, fill="red", width=2, tags="date_line")

# Function to render a simple globe based on the selected season
def render_globe(season):
    canvas.delete("globe")
    radius = 100
    center_x, center_y = 150, 150
    radius_northern = radius
    radius_southern = radius

    canvas.create_arc(
        center_x - radius_northern,
        center_y - radius_northern,
        center_x + radius_northern,
        center_y + radius_northern,
        start=0,
        extent=180,
        outline="black",
        fill=SEASON_COLORS.get(season, "white"),
        tags="globe",
    )

    canvas.create_arc(
        center_x - radius_southern,
        center_y - radius_southern,
        center_x + radius_southern,
        center_y + radius_southern,
        start=0,
        extent=-180,
        outline="black",
        fill=SEASON_COLORS.get(OPPOSITE_SEASON.get(season), "white"),
        tags="globe",
    )

    # Call the Date Line animation function
    animate_date_line(240, 1)  # Start from 0 degrees and increment by 1 degree
    animate_date_line(180, -1)  # Start from 180 degrees and decrement by 1 degree

# UI components for the Season and Location tab
season_label = tk.Label(seasonLocationTab, text='Select a Season:')
season_label.pack()
season_var = tk.StringVar()
season_menu = tk.OptionMenu(seasonLocationTab, season_var, *SEASON_COLORS.keys())
season_menu.pack()

location_label = tk.Label(seasonLocationTab, text='Select a Major City:')
location_label.pack()
location_var = tk.StringVar()
location_menu = tk.OptionMenu(seasonLocationTab, location_var, *location_choices)
location_menu.pack()

open_image_button = tk.Button(
    seasonLocationTab,
    text='Submit',
    command=lambda: (functions.open_image(location_var.get(), result_label), render_globe(season_var.get()))
)
open_image_button.pack()

result_label = tk.Label(seasonLocationTab, text='')
result_label.pack()
canvas = tk.Canvas(seasonLocationTab, width=300, height=300)
canvas.pack()

# UI components for the GPS Data tab
display_gps_button = tk.Button(gpsDataTab, text="Display GPS Data", command=lambda: functions.display_gps_data(gps_data, result_label))
display_gps_button.pack()
result_label = tk.Label(gpsDataTab, text='')
result_label.pack()

# Load GPS data from the file
file_path = "output.txt"
gps_data = functions.read_gps_data(file_path)

gps_location_label = tk.Label(gpsDataTab, text='Select a Major City:')
gps_location_label.pack()
gps_location_var = tk.StringVar()
gps_location_var.set(gps_data.get("Closest City"))
gps_location_menu = tk.OptionMenu(gpsDataTab, gps_location_var, *location_choices)
gps_location_menu.pack()

open_gps_image_button = tk.Button(
    gpsDataTab,
    text='Submit',
    command=lambda: (functions.open_image(gps_location_var.get(), result_label))
)
open_gps_image_button.pack()

# Run the Tkinter main loop
root.mainloop()
