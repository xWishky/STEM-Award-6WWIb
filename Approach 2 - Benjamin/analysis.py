__author__ = "Benjamin Boonen"

import matplotlib
import os
from datetime import datetime
import csv
import pandas as pd
import numpy as np

# Dit is slechts een test, een proof of concept.
# Het document in Approach 1 is het document dat
# uiteindelijk gebruikt is voor het berekenen
# van de eigenlijke resultaten. Dit is een 
# Idea-sketch
# - Benjamin Boonen

data_folder = "./output"
def seconds_since_midnight(t):
    t = datetime.strptime(t, "%H:%M:%S")
    t = t.hour * 3600 + t.minute * 60 + t.second
    return t

def find_hour(sec):
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
    for i, (start, end) in enumerate(lesson_hours, 1):
        lesson_data = (start <= sec < end)
        if lesson_data:
            return i

def get_csv(file, point=None, plot=False):
    df = pd.read_csv(file)
    return df
person = input("person to analyze (0 gives avg): ")
timestamp = seconds_since_midnight(input("timestamp to calculate (in hh:mm:ss): "))
timedev = 60

print(f"seconds since midnight: {timestamp}")

total_devs = []

if person != "0":
    print("searching for", person)
    folder = data_folder + "/" + person
    print(folder)
    day = input("select day: " + str(os.listdir(folder)))
    folder += "/" + day
    print(os.listdir(folder))
    file = f"Lesson_{find_hour(timestamp)}.csv"
    print(file)
    if not(file in os.listdir(folder)):
        os.system("cls")
        print("DATA NOT PRESENT!")
        exit()
    else:
        df = get_csv(f"{folder}/{file}")
        t = df[df["Seconds Since Midnight"] == timestamp].index.values[0]
        start = max(0, t - 60)
        end = min(t + 60, len(df))

        hr_before = []
        for i in range(start, t):
            hr_before.append(int(df.iloc[i, 1]))

        hr_after = []
        for i in range(t, end):
            hr_after.append(int(df.iloc[i, 1]))

        before_mean = np.mean(hr_before)
        after_mean = np.mean(hr_after)
        print(before_mean, after_mean)
        print(abs(after_mean - before_mean))
        total_devs.append(float(after_mean - before_mean))
else:
    day = input("select day: ")
    people = os.listdir("./output/")
    for person in people:
        print("searching for", person)
        folder = data_folder + "/" + person
        if not((folder + "/" + day) in os.listdir(folder)):
            os.system("cls")
            print("DATA NOT PRESENT!")
            continue
        folder += "/" + day
        file = f"Lesson_{find_hour(timestamp)}.csv"
        if not(file in os.listdir(folder)):
            os.system("cls")
            print("DATA NOT PRESENT!")
            continue
        else:
            df = get_csv(f"{folder}/{file}")
            t = df[df["Seconds Since Midnight"] == timestamp].index.values[0]
            start = max(0, t - 60)
            end = min(t + 60, len(df))

            hr_before = []
            for i in range(start, t):
                hr_before.append(int(df.iloc[i, 1]))

            hr_after = []
            for i in range(t, end):
                hr_after.append(int(df.iloc[i, 1]))

            before_mean = np.mean(hr_before)
            after_mean = np.mean(hr_after)
            print(before_mean, after_mean)
            print("WHAA", abs(after_mean - before_mean))
            total_devs.append(after_mean - before_mean)
print(total_devs)
        