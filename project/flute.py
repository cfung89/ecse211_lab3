#! /bin/python3

from utils.brick import EV3UltrasonicSensor
from utils.sound import Sound

# initialize 4 notes we will use
noteA = Sound(duration=0.3, pitch="A4", volume=100)
noteB = Sound(duration=0.3, pitch="B4", volume=100)
noteC = Sound(duration=0.3, pitch="C5", volume=100)
noteD = Sound(duration=0.3, pitch="D5", volume=100)

def play_A():
    noteA.play()
    noteA.wait_done()

def play_B():
    noteB.play()
    noteB.wait_done()

def play_C():
    noteC.play()
    noteC.wait_done()

def play_D():
    noteD.play()
    noteD.wait_done()

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
                pass

if __name__ == "__main__":
    print("Flute subsystem tests")
    ultra = EV3UltrasonicSensor(2)
    run_flute_subsystem(ultra)
