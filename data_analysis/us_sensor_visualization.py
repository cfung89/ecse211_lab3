#!/usr/bin/env python3

"""
This file is used to plot continuous data collected from the ultrasonic sensor.
It should be run on your computer, not on the robot.

Before running this script for the first time, you must install the dependencies
as explained in the README.md file.
"""

from matplotlib import pyplot as plt

US_SENSOR_DATA_FILE = "us_sensor.csv"
DELAY_SEC = 0.01

with open(US_SENSOR_DATA_FILE, "r") as f:
    data = [d.strip("\n").split(",") for d in f.readlines()]

distances = [float(d[0]) for d in data]
notes = [int(d[1]) for d in data]
times = [DELAY_SEC * i for i in range(len(distances))]


# plot the graph of data, juxtasposing the note played and the distance measured
fig, ax1 = plt.subplots()

labels = ["No note", "A", "B", "C", "D"]

color = 'tab:red'
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Note played', color=color)
ax1.plot(times, notes, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_yticks([i for i in range(len(labels))])
ax1.set_yticklabels(labels)

ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Distance (cm)', color=color)  # we already handled the x-label with ax1
ax2.plot(times, distances, color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_yticks([d for d in range(round(max(distances)) + 10) if d % 10 == 0])

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()