__author__ = "Wies Van Lommel"

import glob
import os
import pandas as pd

def to_seconds(h, m, s):
    """Convert the format hh:mm:ss to seconds since midnight"""
    return h * 3600 + m * 60 + s


def calculate_mean(time_range, data_files):
    """Calculate the mean over a given time range"""
    total, count = 0, 0
    for file in data_files:
        df = pd.read_csv(file)
        df = df[(df["Tijd"] >= time_range[0]) & (df["Tijd"] < time_range[1])]
        valid_hr = pd.to_numeric(df["Hartslag"], errors='coerce').dropna()
        total += valid_hr.sum()
        count += valid_hr.count()
    return total / count if count > 0 else None


def calc_differences(date, start_hour):
    time_before = (start_hour - 60, start_hour)  # 1 minute before the starting hour
    time_after = (start_hour, start_hour + 60)  # 1 minute from the starting hour on

    data_map = glob.glob("Data/*")  # Get all the data folders for each person
    all_differences = []  # List containing all the differences in means

    # Loop over all persons data
    for folder in data_map:
        subfolders = glob.glob(f"{folder}/*")  # Get each day from a specific person
        name = os.path.basename(folder).split("-")[-1]  # Get the name off the current person

        # Loop through all data files in a specific day
        for subfolder in subfolders:
            folder_name = os.path.basename(subfolder)  # Get the name of the current folder
            extracted_date = "-".join(folder_name.split("-")[:3])  # Extract the date from the record

            date_without_day = date.rsplit("-", 1)[0]

            if extracted_date == date_without_day:  # Check whether we have the correct folder

                data_files = sorted(glob.glob(f"{subfolder}/*.csv"))  # Get all the data per lesson in a list of CSV files

                mean_before = calculate_mean(time_before, data_files)  # Get the mean of the heart rates 1 minute before the given time
                mean_after = calculate_mean(time_after, data_files)  # Get the mean of the heart rates 1 minute from the given time on

                if mean_before is not None and mean_after is not None:  # Check if both means exist
                    difference = mean_after - mean_before  # Calculate the difference in means
                    all_differences.append((name, difference))  # Add the difference to the list
                else:
                    all_differences.append((name, "No data")) # If no mean could be calculated, add "No data"

    overall_mean = 0
    amt_people_w_data = 0
    for name, diff in all_differences:
        if diff != "No data":
            overall_mean += diff
            amt_people_w_data += 1

    if overall_mean != 0:
        global_mean = overall_mean / amt_people_w_data
    else:
        global_mean = "No data"
    all_differences.append(("", ""))
    all_differences.append(("Global", global_mean))

    return all_differences


# TEST CODE NI MEER NODIG
# date = input("Give a date (dd-mm-yy): ") # Get the date
# start_hour = to_seconds(*map(int, input("Give a starting hour (hh:mm:ss): ").split(":"))) # Get the starting hour and convert it to seconds since midnight
#
# time_before = (start_hour - 60, start_hour)  # 1 minute before the starting hour
# time_after = (start_hour, start_hour + 60)  # 1 minute from the starting hour on
#
# data_map = glob.glob("Data/*") # Get all the data folders for each person
# all_differences = [] # List containing all the differences in means
#
# # Loop over all persons data
# for folder in data_map:
#     subfolders = glob.glob(f"{folder}/*") # Get each day from a specific person
#     name = os.path.basename(folder).split("-")[-1] # Get the name off the current person
#
#     # Loop through all data files in a specific day
#     for subfolder in subfolders:
#         folder_name = os.path.basename(subfolder) # Get the name of the current folder
#         extracted_date = "-".join(folder_name.split("-")[:3]) # Extract the date from the record
#
#         if extracted_date == date: # Check whether we have the correct folder
#
#             data_files = sorted(glob.glob(f"{subfolder}/*.csv")) # Get all the data per lesson in a list of CSV files
#
#             mean_before = calculate_mean(time_before) # Get the mean of the heart rates 1 minute before the given time
#             mean_after = calculate_mean(time_after) #Get the mean of the heart rates 1 minute from the given time on
#
#             if mean_before is not None and mean_after is not None: # Check if both means exist
#                 difference = mean_after - mean_before # Calculate the difference in means
#                 all_differences.append((name, difference)) # Add the difference to the list
#
# # Print each difference in heart rate means per person
# for person, diff in all_differences:
#     print(f"Heart rate difference for {person}: {diff:.2f} bpm")
#
# # Print the overall average difference in means
# overall_diff = sum(d for _, d in all_differences) / len(all_differences) if all_differences else 0
# print(f"Overall average difference: {overall_diff:.2f} bpm")
