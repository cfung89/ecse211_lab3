#! /bin/python3

import threading, time
from utils.brick import Motor, TouchSensor, EV3UltrasonicSensor
from utils.brick import wait_ready_sensors, reset_brick
from drum import run_drum_subsystem
from flute import run_flute_subsystem

TIMEOUT_TOUCH_SENSOR = 0.5

def main():
    # devices
    stop_touch = TouchSensor(4)         # touch sensor for the emergency stop
    ultra = EV3UltrasonicSensor(2)      # ultrasonic sensor for the flute
    drum_touch = TouchSensor(3)         # touch sensor to start/stop the drum
    motor = Motor("A")                  # motor controlling the drum rod

    wait_ready_sensors()
    print("Sensors ready.")

    # Threading Event created in order to stop child threads
    # set main_stop_event so that subsystems can start when threads are started
    main_stop_event = threading.Event()
    main_stop_event.set()

    # Create and start threads
    drum_thread = threading.Thread(target=run_drum_subsystem, args=(motor, drum_touch, main_stop_event))
    flute_thread = threading.Thread(target=run_flute_subsystem, args=(ultra, main_stop_event))
    drum_thread.start()
    flute_thread.start()
    print("Threads started.")

    try:
        while True:
            if stop_touch.is_pressed():             # emergency stop is pressed
                if not (main_stop_event is None):
                    main_stop_event.clear()         # send signal to child threads
                raise KeyboardInterrupt("Emergency stop activated.")    # stop main process
            time.sleep(TIMEOUT_TOUCH_SENSOR)

            if not flute_thread.is_alive():         # restart flute thread if it threw an exception
                print("Restarting flute thread.")
                flute_thread = threading.Thread(target=run_flute_subsystem, args=(ultra, main_stop_event))
                flute_thread.start()

    except KeyboardInterrupt as e:
        print(e)

    finally:
        # wait for threads to thread to finish executing
        drum_thread.join()
        flute_thread.join()
        reset_brick()

        print("Threads stopped and cleaned up.")
        print("Exiting...")

if __name__ == "__main__":
    main()
