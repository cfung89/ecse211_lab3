#! /bin/python3

from utils.brick import EV3UltrasonicSensor
from utils.sound import Sound
import time

DELAY_US = 0.01 # delay time between measurements

# initialize 4 notes we will use
noteA = Sound(duration=1, pitch="A4", volume=100)
noteB = Sound(duration=1, pitch="B4", volume=100)
noteC = Sound(duration=1, pitch="C5", volume=100)
noteD = Sound(duration=1, pitch="D5", volume=100)

def play_A():
    """Plays the note A"""
    if not noteA.is_playing():
        noteA.play() # no wait done so will play until gets stopped
    noteB.stop()
    noteC.stop()
    noteD.stop()

def play_B():
    """Plays the note B"""
    if not noteB.is_playing():
        noteB.play() # no wait done so will play until gets stopped
    noteA.stop()
    noteC.stop()
    noteD.stop()

def play_C():
    """Plays the note C"""
    if not noteC.is_playing():
        noteC.play() # no wait done so will play until gets stopped
    noteA.stop()
    noteB.stop()
    noteD.stop()

def play_D():
    """Plays the note D"""
    if not noteD.is_playing():
        noteD.play() # no wait done so will play until gets stopped
    noteA.stop()
    noteB.stop()
    noteC.stop()

def play_none():
    """Plays no notes"""
    noteA.stop()
    noteB.stop()
    noteC.stop()
    noteD.stop()

def run_flute_subsystem(ultra: EV3UltrasonicSensor):
    while True:
        distance = ultra.get_cm()
        if distance is not None:
            if 5 <= distance < 15:
                # play an A
                play_A()
            elif 15 <= distance < 25:
                # play a B
                play_B()
            elif 25 <= distance < 35: 
                # play a C
                play_C()
            elif 35 <= distance < 45:
                # play a D
                play_D()
            else:
                # play nothing
                play_none()
        time.sleep(DELAY_US)

if __name__ == "__main__":
    print("Flute subsystem tests")
    ultra = EV3UltrasonicSensor(2)
    run_flute_subsystem(ultra)
