#! /bin/python3

import threading, time
from utils.brick import Motor, TouchSensor

# constants for motor angles and delays
ANGLE_ABSOLUTE_RESET = 0 # always reset motor to this absolute position
ANGLE_RELATIVE_NOTE_START = 15 # motor angle at the start of a drum note
DELAY_QUARTER = 0.30
DELAY_EIGHTH_NOTE = DELAY_QUARTER / 2
DELAY_TRIPLET = DELAY_QUARTER / 3
TIMEOUT_TOUCH_SENSOR = 0.5

def run_drum_subsystem(motor: Motor, drum_touch: TouchSensor, main_stop_event: threading.Event):
    """
    Run the drum subsystem: playing is toggled by pressing the drum touch sensor.
    """
    reset_drum(motor)

    # use Event object to track if drum is playing
    global drum_stop_event
    drum_stop_event = threading.Event()

    t = None
    while main_stop_event.is_set():
        if drum_touch.is_pressed():
            if drum_stop_event.is_set():
                # reset the drum to prepare for the next time it starts playing
                drum_stop_event.clear()
                if not (t is None):
                    t.join()
                reset_drum(motor)
            else:
                # create and start drum thread
                t = threading.Thread(target=play_drum_constant, args=(motor, DELAY_EIGHTH_NOTE))
                drum_stop_event.set()
                t.start()

            # prevent sensor from registering multiple touches if it's being held
            time.sleep(TIMEOUT_TOUCH_SENSOR)
    drum_stop_event.clear()
    if not (t is None) and t.is_alive():
        t.join()
    reset_drum(motor)

def reset_drum(motor: Motor):
    """
    Resets the drum motor.
    """
    motor.set_position(ANGLE_ABSOLUTE_RESET)
    return

def play_drum_triplet(motor: Motor, n_times: int):
    """
    Plays a triplet on the drum `n_times` number of times.
    """
    for _ in range(n_times):
        for _ in range(3):
            play_drum_note(motor, DELAY_TRIPLET)

    return

def play_drum_eighth_note(motor: Motor, n_times: int):
    """
    Plays an eighth note on the drum `n_times` number of times.
    """
    for _ in range(n_times):
        play_drum_note(motor, DELAY_EIGHTH_NOTE)

    return

def play_drum_note(motor: Motor, delay: float):
    """
    Plays a note with the specified delay once.
    """
    motor.set_position_relative(-1 * ANGLE_RELATIVE_NOTE_START)
    time.sleep(delay)

    motor.set_position_relative(ANGLE_RELATIVE_NOTE_START)
    time.sleep(delay)

    return

def play_drum_constant(motor: Motor, delay: float):
    """
    Plays a note with the specified delay repeatedly.
    """
    while not (drum_stop_event is None) and drum_stop_event.is_set():
        motor.set_position_relative(-1 * ANGLE_RELATIVE_NOTE_START)
        time.sleep(delay)

        motor.set_position_relative(ANGLE_RELATIVE_NOTE_START)
        time.sleep(delay)

def reset_position(motor: Motor):
    motor.reset_position()
    assert motor.get_position() == 0

if __name__ == "__main__":
    from utils.brick import wait_ready_sensors

    print("Drum subsystem tests")
    drum_touch = TouchSensor(3)
    motor = Motor("A")
    wait_ready_sensors()
    main_stop_event = threading.Event()
    main_stop_event.set()
    try:
        run_drum_subsystem(motor, drum_touch, main_stop_event)
    except KeyboardInterrupt:
        pass
