__author__ = "Benjamin Boonen"

import os
import csv
from datetime import datetime, timedelta
import pandas as pd

def process_csv(file_path):
    # Metadata halen uit de header
    file_name = os.path.basename(file_path)
    parts = file_name.split("_")
    person_name = f"{parts[0]}_{parts[1]}"
    date_str = parts[2]  # standaardformaat voor JJJJ-MM-DD
    start_time_str = parts[3].split(".")[0].replace("-", ":")  # omzetten in YYYY-MM-DD HH:MM
    
    # Omzetten naar seconden sinds middernacht
    start_time = datetime.strptime(start_time_str, "%H:%M:%S")
    start_seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second
    
    # Csv laden (skip de metadata)
    df = pd.read_csv(file_path, skiprows=2)
    df = df.iloc[:, [1, 2]]  # Hebben slechts 2 kolommen nodig
    df.columns = ["Time", "HR"]
    
    processed_data = []
    
    for _, row in df.iterrows():
        try:
            # van HH:MM:SS naar seconden sinds begin van meting
            time_since_start = sum(int(x) * 60**i for i, x in enumerate(reversed(row["Time"].split(":"))))
            heartbeat = int(row["HR"])

            # absolute tijd berekenen (tijd sinds middernacht)
            seconds_since_midnight = start_seconds + time_since_start
            time_since_midnight_str = str(timedelta(seconds=seconds_since_midnight))

            processed_data.append([seconds_since_midnight, heartbeat, time_since_midnight_str])
        except (ValueError, AttributeError):
            continue  # negeer errors
    
    return person_name, date_str, processed_data

def split_and_save(processed_data, person_name, date_str):
    # lesuren structuur in seconden sinds middernacht
    lesson_hours = [
        (8*3600 + 25*60, 9*3600 + 15*60),
        (9*3600 + 15*60, 10*3600 + 5*60),
        (10*3600 + 20*60, 11*3600 + 10*60),
        (11*3600 + 10*60, 12*3600),
        (13*3600, 13*3600 + 50*60),
        (13*3600 + 50*60, 14*3600 + 40*60),
        (14*3600 + 55*60, 15*3600 + 45*60),
        (15*3600 + 45*60, 16*3600 + 35*60)
    ]
    
    # output folder
    output_dir = f"output/{person_name}/{date_str}"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, (start, end) in enumerate(lesson_hours, 1):
        lesson_data = [row for row in processed_data if start <= row[0] < end]
        if lesson_data:
            lesson_file = f"{output_dir}/Lesson_{i}.csv"
            with open(lesson_file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Seconds Since Midnight", "Heartbeat", "Time HH:MM:SS"])
                writer.writerows(lesson_data)

def process_all_files(folder_path):
    # loop doorheen alle csv-bestanden
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".CSV"):
            file_path = os.path.join(folder_path, file_name)
            try:
                person_name, date_str, data = process_csv(file_path)
                split_and_save(data, person_name, date_str)
                print(f"Verwerkt: {file_name}")
            except Exception as e:
                print(f"Error bij verwerking van {file_name}: {e}")

if __name__ == "__main__":
    folder_path = "./data"