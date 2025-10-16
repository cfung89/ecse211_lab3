#! /bin/python3

import threading, time
import simpleaudio as sa
from utils.brick import EV3UltrasonicSensor
from utils.sound import Sound

DELAY_US = 0.01 # delay time between measurements
THETA = 1 # threshold in cm for transitions between notes

# initialize 4 notes we will use
noteA = Sound(duration=0.5, pitch="A4", volume=80)
noteB = Sound(duration=0.5, pitch="B4", volume=80)
noteC = Sound(duration=0.5, pitch="C5", volume=80)
noteD = Sound(duration=0.5, pitch="D5", volume=80)

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

NOTES = {
    "A": play_A,
    "B": play_B,
    "C": play_C,
    "D": play_D,
    "X": play_none
}

def run_flute_subsystem(ultra: EV3UltrasonicSensor, main_stop_event: threading.Event):
    # to smooth out transitions, need to read 5 readings in a row in that category
    prev = "X"

    while main_stop_event.is_set():
        distance = ultra.get_cm()
        if distance is not None:
            try:
                if 5 <= distance < 15:
                    current = "A"
                    if (abs(distance-5) < THETA and prev == "X") or (abs(distance-15) < THETA and prev == "B"):
                        # play previous note while waiting to stabilize in between transitions
                        NOTES[prev]()
                    else:
                        NOTES[current]()
                elif 15 <= distance < 25:
                    current = "B"
                    if (abs(distance-15) < THETA and prev == "A") or (abs(distance-25) < THETA and prev == "C"):
                        # play previous note while waiting to stabilize in between transitions
                        NOTES[prev]()
                    else:
                        NOTES[current]()
                elif 25 <= distance < 35: 
                    current = "C"
                    if (abs(distance-25) < THETA and prev == "B") or (abs(distance-35) < THETA and prev == "D"):
                        # play previous note while waiting to stabilize in between transitions
                        NOTES[prev]()
                    else:
                        NOTES[current]()
                elif 35 <= distance < 45:
                    current = "D"
                    if (abs(distance-35) < THETA and prev == "C") or (abs(distance-45) < THETA and prev == "X"):
                        # play previous note while waiting to stabilize in between transitions
                        NOTES[prev]()
                    else:
                        NOTES[current]()
                else:
                    current = "X"
                    NOTES[current]()
                prev = current
            except sa.SimpleaudioError:
                return
        time.sleep(DELAY_US)

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
