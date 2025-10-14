#! /bin/python3

import threading, signal, time
from utils.brick import Motor, TouchSensor, EV3UltrasonicSensor
from utils.brick import wait_ready_sensors
from drum import run_drum_subsystem
from flute import run_flute_subsystem

TIMEOUT_TOUCH_SENSOR = 0.5

def main():
    # devices
    stop_touch = TouchSensor(4) # touch sensor for the emergency stop
    ultra = EV3UltrasonicSensor(2) # ultrasonic sensor for the flute
    drum_touch = TouchSensor(3) # touch sensor to start/stop the drum
    motor = Motor("A") # motor controlling the drum rod

    wait_ready_sensors()

    drum_thread = threading.Thread(target=run_drum_subsystem, args=(motor, drum_touch))
    flute_thread = threading.Thread(target=run_flute_subsystem, args=(ultra,))

    drum_thread.start()
    flute_thread.start()

    try:
        while True:
            if stop_touch.is_pressed():
                raise KeyboardInterrupt("Emergency stop activated.")
            time.sleep(TIMEOUT_TOUCH_SENSOR)

    except KeyboardInterrupt as e:
        print(e)

    finally:
        drum_thread_id = drum_thread.ident
        flute_thread_id= flute_thread.ident

        if not(drum_thread_id is None):
            signal.pthread_kill(drum_thread_id, signal.SIGTERM)

        if not(flute_thread_id is None):
            signal.pthread_kill(flute_thread_id, signal.SIGTERM)

        drum_thread.join()
        flute_thread.join()

    print("Threads stopped and cleaned up.")
    print("Exiting...")

if __name__ == "__main__":
    main()
