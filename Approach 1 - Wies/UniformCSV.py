__author__ = "Wies Van Lommel"

import glob
import pandas as pd
import os

# A list containing all names of the people of which we have data
names = ["Wies", "Benji", "Kyle", "Luca", "Lore"]
lesson_hours_per_day = {
    "Maandag": [
        (30300, 33300),  # 08:25 - 09:15
        (33300, 36300),  # 09:15 - 10:05
        (37200, 40200),  # 10:20 - 11:10
        (40200, 43200),  # 11:10 - 12:00
        (46800, 49800),  # 13:00 - 13:50
        (49800, 52800),  # 13:50 - 14:40
        (53700, 56700)   # 14:55 - 15:45
    ],
    "Dinsdag": [
        (30300, 33300), # 08:25 - 09:15
        (33300, 36300), # 09:15 - 10:05
        (37200, 40200), # 10:20 - 11:10
        (40200, 43200), # 11:10 - 12:00
        (46800, 49800), # 13:00 - 13:50
        (49800, 52800), # 13:50 - 14:40
        (53700, 56700)  # 14:55 - 15:45
    ],
    "Woensdag": [
        (30300, 33300), # 08:25 - 09:15
        (33300, 36300), # 09:15 - 10:05
        (37200, 40200), # 10:20 - 11:10
        (40200, 43200)  # 11:10 - 12:00
    ],
    "Donderdag": [
        (30300, 33300), # 08:25 - 09:15
        (33300, 36300), # 09:15 - 10:05
        (37200, 40200), # 10:20 - 11:10
        (40200, 43200), # 11:10 - 12:00
        (46800, 49800), # 13:00 - 13:50
        (49800, 52800), # 13:50 - 14:40
        (53700, 56700), # 14:55 - 15:45
        (56700, 59700)  # 15:45 - 16:35
    ],
    "Vrijdag": [
        (30300, 33300), # 08:25 - 09:15
        (33300, 36300), # 09:15 - 10:05
        (37200, 40200), # 10:20 - 11:10
        (40200, 43200), # 11:10 - 12:00
        (46800, 49800), # 13:00 - 13:50
        (49800, 52800), # 13:50 - 14:40
        (53700, 56700)  # 14:55 - 15:45
    ]
}

def to_seconds(h, m, s):
    """Convert the format hh:mm:ss to seconds since midnight"""
    return h * 3600 + m * 60 + s


def to_hms(seconds):
    """Convert seconds since midnight to the hh:mm:ss format"""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"


def process_csv(csv_files, name, day_name, day_folder):
    """Create a CSV file per lesson hour"""

    lesson_hours = lesson_hours_per_day.get(day_name, []) # Get the lesson hours for the specific day

    data = [[] for _ in range(len(lesson_hours))] # List that contains all data for each hour
    csv_index = 0 # Index of the current CSV file

    # Loop over all CSV files of the data from one day
    while csv_index < len(csv_files):

        current_csv = pd.read_csv(csv_files[csv_index]) # Read the current CSV file
        start_hour = to_seconds(*list(map(int, current_csv["Start time"].iloc[0].split(":")))) # Get the starting hour and convert it to time in seconds

        # Loop over all datapoints in the current CSV file
        for i in range(len(current_csv["Date"][2:])):

            time = to_seconds( *list(map(int, current_csv["Sport"][2:].iloc[i].split(":") ))) + start_hour # Get the time at which a datapoint is recorded

            # Loop over all hours of the current day
            for hour, (start, end) in enumerate(lesson_hours):

                # Check if the current time is located between start and end of the current hour to find in which sub-list we have to add it
                if start <= time <= end:
                    heart_rate = current_csv["Date"][2:].iloc[i] # Extract the heart rate from the CSV file
                    if pd.isna(heart_rate): # If the heart rate is NaN, add "No data" to the list
                        data[hour].append((time, None, to_hms(time)))
                    else: # Add the heart rate and the time at which it was recorded to the correct sub-list
                        data[hour].append( (time, heart_rate, to_hms(time)) )

        csv_index += 1 # If the CSV is fully read, go to the next one

    # Loop over all hours in the current day
    for hour, (start, end) in enumerate(lesson_hours):

        # Loop over the amount of datapoints we should have in an hour
        for i in range(end - start):
            lesson_time = start + i # Get the time since the start of the lesson

            if not any(t[0] == lesson_time for t in data[hour]): # Fill missing data with "No data"
                data[hour].insert(i, (lesson_time, None, to_hms(lesson_time)) )

        # Write everything to a CSV file
        df = pd.DataFrame(data[hour], columns=["Tijd", "Hartslag", "HMS"])
        df.to_csv(f"{day_folder}/{day_name}-Lesuur-{hour + 1}-{name}.csv", index=False)


# Loop over all the names of the persons of which we have collected data
for name in names:

    data_person_days = glob.glob(f"Personen-Data/Data-Hartslag-{name}/*") # Get all folders inside the folder containing the persons data

    person_folder = f"Data-(NaN)/Data-Hartslag-Test-{name}" # Path for the folder in which we will store the output
    os.makedirs(person_folder, exist_ok=True) # Create the directory if it doesn't already exist

    # Loop over each day in which we collected data for the specific person
    for day_dir in data_person_days:
        folder_name = os.path.basename(day_dir) # Get the folder name
        day_name = folder_name.split("-")[-1] # Extract the day name from the folder name

        day_folder = os.path.join(person_folder, folder_name) # Full path to the output folder of the day
        os.makedirs(day_folder, exist_ok=True) # Create the directory for the day if it doesn't already exist

        data_files = glob.glob(f"{day_dir}/*.csv") # Get a list of all CSV files for that specific day
        process_csv(data_files, name, day_name, day_folder) # Process all data and convert it to a CSV file
