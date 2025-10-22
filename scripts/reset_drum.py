from project.drum import *
from project.utils.brick import wait_ready_sensors, TouchSensor, Motor

if __name__ == "__main__":
    print("Drum subsystem tests")
    drum_touch = TouchSensor(3)
    motor = Motor("A")
    wait_ready_sensors()
    reset_position(motor)
