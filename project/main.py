#! /bin/python3

from utils.brick import wait_ready_sensors
from subsystems.drum import run_drum_subsystem

def main():
    wait_ready_sensors()

    run_drum_subsystem()

if __name__ == "__main__":
    main()
