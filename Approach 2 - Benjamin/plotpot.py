import os
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Button
import glob

# List of names to iterate through
names = glob.glob("output/*")
name = names[0]
print(name)

# Retrieve all available days in the data of the selected person
# We assume here that every folder has the same structure
days = glob.glob(f"{name}/*")
print(days)

amt_days = len(days)
print(amt_days)

day_index = 0
current_day = os.path.basename(days[day_index])

# Get all available CSV files for the selected day
data_hours = glob.glob(f"{name}/{current_day}/*.csv")
hour_index = 0

# Initiate the matplotlib figure and axis, add some room on the bottom to create space for the buttons
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)


def update_plot():
    """Update the plot with the new heart rate data from the selected CSV file"""
    global current_day, data_hours
    data_hours = glob.glob(f"{name}/{current_day}/*.csv")

    ax.clear() # Reset the plot
    ax.set_title(f"{current_day} - {name}\n lesuur: {hour_index+1}") # Adjust the title for the correct person and day

    # Get all data for the hour that is selected, and convert all the heart rate values to floats
    df = pd.read_csv(data_hours[hour_index])
    heart_beat = list(map(float, df["Heartbeat"][2:]))

    ax.plot(heart_beat, color='red', linewidth='0.75') # Plot the heart data

    # Set labels for x- and y-axis
    ax.set_xlabel("Tijd (in seconden)")
    ax.set_ylabel("Hartslag (in bpm)")

    ax.grid(True) # Show a grid

    fig.canvas.draw() # Redraw the canvas


def next_day(event):
    """Switch over to the next available day and update the plot"""
    global day_index, hour_index, current_day, data_hours

    # Switch to the next day
    day_index = (day_index + 1) % amt_days
    current_day = os.path.basename(days[day_index])

    # Update the available hours, which are CSV files, for the new day
    data_hours = glob.glob(f"{name}/{current_day}/*.csv")
    hour_index = 0

    update_plot() # Update the plot


def next_hour(event):
    """Switch over to the next available hour in the chosen day and update the plot"""
    global hour_index

    # Switch to the next hour
    hour_index = (hour_index + 1) % len(data_hours)

    update_plot() # Update the plot

def next_person(event):
    """Switch over to the next available person and update the plot"""
    global name, day_index, hour_index, current_day, days, data_hours, amt_days

    # Switch to the next person
    name = names[(names.index(name) + 1) % len(names)]

    # Start at the first day and hour of the persons data
    day_index = 0
    hour_index = 0

    # Load the available days for the chosen person
    days = glob.glob(f"{name}/*")
    amt_days = len(days)
    current_day = os.path.basename(days[day_index])

    # Get the available hours for the new day
    data_hours = glob.glob(f"{name}/{current_day}/*.csv")

    update_plot() # Update the plot


# Create and add the button to switch hours
ax_next_hour = plt.axes([0.75, 0.05, 0.2, 0.075])
btn_next_hour = Button(ax_next_hour, "Volgend lesuur")
btn_next_hour.on_clicked(next_hour)

# Create and add the button to switch days
ax_next_day = plt.axes([0.05, 0.05, 0.2, 0.075])
btn_next_day = Button(ax_next_day, "Volgende dag")
btn_next_day.on_clicked(next_day)

# Create and add the button to switch persons
ax_next_person = plt.axes([0.05, 0.15, 0.2, 0.075])
btn_next_person = Button(ax_next_person, "Volgend persoon")
btn_next_person.on_clicked(next_person)

update_plot() # Update the plot
plt.show() # Show the plot
