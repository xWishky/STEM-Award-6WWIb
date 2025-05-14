import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from CalcMeans import calc_differences, to_seconds


# Variables for styles
BG_COLOR = "#55c0de"
FG_COLOR = "#231b3b"
ACCENT_COLOR = "#231b3b"

FONT_TITLE = ("Helvetica", 24, "bold")
FONT_LABEL = ("Helvetica", 14)
FONT_INPUT = ("Helvetica", 16)


# Create the main window
root = tk.Tk()
root.title("Calculate means")
root.geometry("850x800")
root.configure(bg=BG_COLOR)

# Add the title
title = tk.Label(root, text="Calculate means for each person", font=FONT_TITLE, fg=ACCENT_COLOR, bg=BG_COLOR)
title.pack(pady=30)

# Sila logo in the corner
img = ImageTk.PhotoImage(Image.open("Assets/SamenSila.png").resize((204, 75)))
logo = tk.Label(root, image=img, bg=BG_COLOR)
logo.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)


# Create a frame containing every widget
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(pady=20)

# Add a label above the dropdown menu for date selection
tk.Label(main_frame, text="Select the date you want to analyse", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR).pack(pady=(30, 5))

selected_date = tk.StringVar(value="Select a date") # Set the placeholder for the dropdown menu
date_options = ["04-02-25-Dinsdag", "05-02-25-Woensdag", "06-02-25-Donderdag", "10-02-25-Maandag"] # All the available dates

# Add a dropdown menu for date selection
dropdown = tk.OptionMenu(main_frame, selected_date, *date_options)
dropdown.config(font=FONT_INPUT, width=20, bg="white", fg=FG_COLOR, highlightthickness=1)
dropdown.pack(pady=(0, 40))


# Add a label above the HH:MM:SS inputs
time_label = tk.Label(main_frame, text="Select the time of day you want to analyse", font=FONT_LABEL, bg=BG_COLOR, fg=FG_COLOR)
time_label.pack(pady=(0, 10))

# Create a frame containing all the input fields for the HH:MM:SS
time_frame = tk.Frame(main_frame, bg=BG_COLOR)
time_frame.pack(pady=10)

# Define the styles for the HH:MM:SS inputs
spinbox_style = {"width": 4, "font": FONT_INPUT, "justify": "center"}

# Create a field for the desired hour
hour_spin = tk.Spinbox(time_frame, from_=0, to=24, format="%02.0f", **spinbox_style)
hour_spin.pack(side=tk.LEFT)
tk.Label(time_frame, text="h :", font=FONT_INPUT, bg=BG_COLOR).pack(side=tk.LEFT)

# Create a field for the desired minutes
minute_spin = tk.Spinbox(time_frame, from_=0, to=59, format="%02.0f", **spinbox_style)
minute_spin.pack(side=tk.LEFT)
tk.Label(time_frame, text="m :", font=FONT_INPUT, bg=BG_COLOR).pack(side=tk.LEFT)

# Create a field for the desired seconds
second_spin = tk.Spinbox(time_frame, from_=0, to=59, format="%02.0f", **spinbox_style)
second_spin.pack(side=tk.LEFT)
tk.Label(time_frame, text="s", font=FONT_INPUT, bg=BG_COLOR).pack(side=tk.LEFT)


def show_results():
    """Display the results with a treeview"""

    # Get all the filled in data from the input fields
    date = selected_date.get()
    h = int(hour_spin.get())
    m = int(minute_spin.get())
    s = int(second_spin.get())
    seconds = to_seconds(h, m, s)

    # Calculate the results
    results = calc_differences(date, seconds)

    # Remove old data from the frame
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Adapt the style of the treeview
    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Helvetica", 11))
    style.configure("Custom.Treeview.Heading", font=("Helvetica", 12, "bold"))

    # Instantiate a treeview
    tree = ttk.Treeview(result_frame, columns=("name", "diff"), show="headings", height=8, style="Custom.Treeview")
    tree.heading("name", text="Naam")
    tree.heading("diff", text="Gemiddelde bpm")

    tree.column("name", width=100, anchor="center")
    tree.column("diff", width=150, anchor="center")

    # For every person there is a result for we add it to the treeview
    for name, diff in results:

        # If there is no data for a specific person, display No data, else display the mean
        if diff == "":
            tree.insert("", "end", values=("", ""))
        else:
            data_person = "No data" if diff == "No data" else f"{diff:.2f} bpm"
            tree.insert("", "end", values=(name, data_person))

    # Display the tree
    tree.pack()


def on_submit():
    """Function handling the submit button clicks"""
    show_results()


# Create a button to submit the given data
submit_button = tk.Button(main_frame, text="Submit", font=FONT_INPUT, width=20, bg="white", fg=FG_COLOR, command=on_submit)
submit_button.pack(pady=(30, 10))

# Add a frame containing the results
result_frame = tk.Frame(main_frame, bg=BG_COLOR)
result_frame.pack(pady=30)

root.mainloop()