#! /bin/python3

from utils.brick import EV3UltrasonicSensor
from utils.sound import Sound

noteA = Sound(duration=0.3, pitch="A4", volume=100)

def run_flute_subsystem(ultra: EV3UltrasonicSensor):
    return

if __name__ == "__main__":
    print("Flute subsystem tests")
    ultra = EV3UltrasonicSensor(2)
