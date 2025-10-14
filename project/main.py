from utils.brick import wait_ready_sensors
from subsystems.drum import run_drum_subsystem

wait_ready_sensors()

run_drum_subsystem()