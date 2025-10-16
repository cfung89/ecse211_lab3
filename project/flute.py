#! /bin/python3

from utils.brick import EV3UltrasonicSensor
from utils.sound import Sound
import time

DELAY_US = 0.01 # delay time between measurements
THRES = 1 # threshold in cm for transitions between notes

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

NOTES = {
    "A": play_A,
    "B": play_B,
    "C": play_C,
    "D": play_D,
    "X": play_none
}

def run_flute_subsystem(ultra: EV3UltrasonicSensor):
    # to smooth out transitions, need to read 5 readings in a row in that category
    prev = "X" 

    while True:
        distance = ultra.get_cm()
        if distance is not None:
            if 5 <= distance < 15:
                current = "A"
                if (abs(distance-5) < THRES and prev == "X") or (abs(distance-15) < THRES and prev == "B"):
                    # play previous note while waiting to stabilize in between transitions
                    NOTES[prev]()
                else:
                    NOTES[current]()
            elif 15 <= distance < 25:
                current = "B"
                if (abs(distance-15) < THRES and prev == "A") or (abs(distance-25) < THRES and prev == "C"):
                    # play previous note while waiting to stabilize in between transitions
                    NOTES[prev]()
                else:
                    NOTES[current]()
            elif 25 <= distance < 35: 
                current = "C"
                if (abs(distance-25) < THRES and prev == "B") or (abs(distance-35) < THRES and prev == "D"):
                    # play previous note while waiting to stabilize in between transitions
                    NOTES[prev]()
                else:
                    NOTES[current]()
            elif 35 <= distance < 45:
                current = "D"
                if (abs(distance-35) < THRES and prev == "C") or (abs(distance-45) < THRES and prev == "X"):
                    # play previous note while waiting to stabilize in between transitions
                    NOTES[prev]()
                else:
                    NOTES[current]()
            else:
                current = "X"
                NOTES[current]()
            prev = current
        time.sleep(DELAY_US)

if __name__ == "__main__":
    print("Flute subsystem tests")
    ultra = EV3UltrasonicSensor(2)
    run_flute_subsystem(ultra)
