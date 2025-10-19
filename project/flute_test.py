#! /bin/python3

import threading, time
import simpleaudio as sa
from utils.brick import EV3UltrasonicSensor
from utils.sound import Sound
import time
from statistics import mode

DELAY_US = 0.01 # delay time between measurements
THETA = 1 # threshold in cm for transitions between notes
WINDOW_SIZE = 4 # size of sliding window for moving median
FILE = "../data_analysis/us_sensor_ordered.csv" # file name for csv for ordered notes test
# FILE = "../data_analysis/us_sensor_unordered.csv" # file name for csv for unordered notes test
 
# initialize 4 notes we will use
noteA = Sound(duration=0.5, pitch="A4", volume=100)
noteB = Sound(duration=0.5, pitch="B4", volume=100)
noteC = Sound(duration=0.5, pitch="C5", volume=100)
noteD = Sound(duration=0.5, pitch="D5", volume=100)

def play_A():
    """Plays the note A"""
    if not noteA.is_playing():
        noteA.play() # no wait done so will play until gets stopped
    else: # if same note playing, stop and start to reset the sound to avoid choppiness
        noteA.stop()
        time.sleep(0.2)
        noteA.play()
    noteB.stop()
    noteC.stop()
    noteD.stop()

def play_B():
    """Plays the note B"""
    if not noteB.is_playing():
        noteB.play() # no wait done so will play until gets stopped
    else: # if same note playing, stop and start to reset the sound to avoid choppiness
        noteB.stop()
        time.sleep(0.2)
        noteB.play()
    noteA.stop()
    noteC.stop()
    noteD.stop()

def play_C():
    """Plays the note C"""
    if not noteC.is_playing():
        noteC.play() # no wait done so will play until gets stopped
    else: # if same note playing, stop and start to reset the sound to avoid choppiness
        noteC.stop()
        time.sleep(0.2)
        noteC.play()
    noteA.stop()
    noteB.stop()
    noteD.stop()

def play_D():
    """Plays the note D"""
    if not noteD.is_playing():
        noteD.play()
    else: # if same note playing, stop and start to reset the sound to avoid choppiness
        noteD.stop()
        time.sleep(0.2)
        noteD.play()
    noteA.stop()
    noteB.stop()
    noteC.stop()

def play_none():
    """Plays no notes"""
    noteA.stop()
    noteB.stop()
    noteC.stop()
    noteD.stop()

def move_window(n: int, window: list):
    """Moves the sliding window by adding one new value."""
    window.pop(0)
    window.append(n)

NOTES = {
    0: play_none,
    1: play_A,
    2: play_B,
    3: play_C,
    4: play_D
}

def run_flute_subsystem(ultra: EV3UltrasonicSensor, main_stop_event: threading.Event):
    """Runs flute subsystem and note playing algorithm. Writes to a CSV file the distance and note pairs if write is True (default False)."""
    # to smooth out transitions, need to read 5 readings in a row in that category
    prev = 0
    current = 0
    window = [0 for _ in range(WINDOW_SIZE)] # sliding window for computing median

    try:
        output_file = open(FILE, "w")

        while main_stop_event.is_set():
            distance = ultra.get_cm()
            if distance is not None:
                try:
                    if 5 <= distance < 15:
                        current = 1
                        move_window(current, window)
                        if (abs(distance-5) < THETA and prev == 0) or (abs(distance-15) < THETA and prev == 2):
                            # play median while waiting to stabilize in between transitions
                            NOTES[mode(window)]()
                        else:
                            NOTES[current]()
                    elif 15 <= distance < 25:
                        current = 2
                        move_window(current, window)
                        if (abs(distance-15) < THETA and prev == 1) or (abs(distance-25) < THETA and prev == 3):
                            # play previous note while waiting to stabilize in between transitions
                            NOTES[mode(window)]()
                        else:
                            NOTES[current]()
                    elif 25 <= distance < 35: 
                        current = 3
                        move_window(current, window)
                        if (abs(distance-25) < THETA and prev == 2) or (abs(distance-35) < THETA and prev == 4):
                            # play previous note while waiting to stabilize in between transitions
                            NOTES[mode(window)]()
                        else:
                            NOTES[current]()
                    elif 35 <= distance < 45:
                        current = 4
                        move_window(current, window)
                        if (abs(distance-35) < THETA and prev == 3) or (abs(distance-45) < THETA and prev == 0):
                            # play previous note while waiting to stabilize in between transitions
                            NOTES[mode(window)]()
                        else:
                            NOTES[current]()
                    else:
                        current = 0
                        move_window(current, window)
                        if (abs(distance-5) < THETA and prev == 1) or (abs(distance-45) < THETA and prev == 4):
                            # play previous note while waiting to stabilize in between transitions
                            NOTES[mode(window)]()
                        else:
                            NOTES[current]()
                    prev = current

                    # write to csv file
                    output_file.write(f"{distance},{current}\n")
                
                except Exception as e:
                    print(f"{e}\n")
                    return
                
                prev = current
            time.sleep(DELAY_US)
    finally:
        print("Done collecting US distance samples")
        output_file.close()


if __name__ == "__main__":
    from utils.brick import wait_ready_sensors

    print("Flute subsystem tests")
    ultra = EV3UltrasonicSensor(2)
    wait_ready_sensors()
    main_stop_event = threading.Event()
    main_stop_event.set()
    try:
        run_flute_subsystem(ultra, main_stop_event)
    except KeyboardInterrupt:
        pass
