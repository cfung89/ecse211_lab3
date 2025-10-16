#! /bin/python3

from utils.brick import EV3UltrasonicSensor
from utils.sound import Sound
import time

DELAY_US = 0.01 # delay time between measurements

# initialize 4 notes we will use
noteA = Sound(duration=1, pitch="A4", volume=80)
noteB = Sound(duration=1, pitch="B4", volume=80)
noteC = Sound(duration=1, pitch="C5", volume=80)
noteD = Sound(duration=1, pitch="D5", volume=80)

# store notes in dictionary for easier access
NOTES = {
    "A": noteA,
    "B": noteB,
    "C": noteC,
    "D": noteD
}

def run_flute_subsystem(ultra: EV3UltrasonicSensor):
    current = None # store the current note to play
    next = None # stores the next note to play

    while True:
        distance = ultra.get_cm()
        if distance is not None:
            if 5 <= distance < 15:
                # play an A
                next = "A"
            elif 15 <= distance < 25:
                # play a B
                next = "B"
            elif 25 <= distance < 35: 
                # play a C
                next = "C"
            elif 35 <= distance < 45:
                # play a D
                next = "D"
            else:
                # play nothing
                next = None
        if next != current: 
            # play new note if it changed
            if current:
                # stop old note
                NOTES[current].stop()
            if next:
                # start playing new note with repeat and interval silence 0
                NOTES[next].repeat_sound(100)

            current = next
        time.sleep(DELAY_US)

if __name__ == "__main__":
    print("Flute subsystem tests")
    ultra = EV3UltrasonicSensor(2)
    run_flute_subsystem(ultra)
