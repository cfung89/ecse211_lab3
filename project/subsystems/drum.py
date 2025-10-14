import time
from utils.brick import Motor, TouchSensor

# constants for motor angles and delays
ANGLE_ABSOLUTE_RESET = 4 # always reset motor to this absolute position
ANGLE_RELATIVE_NOTE_START = 25 # motor angle at the start of a drum note
ANGLE_ABSOLUTE_NOTE_END = 11 # at end of a drum note
DELAY_TRIPLET = 0.10
DELAY_EIGHTH_NOTE = 3 * DELAY_TRIPLET
TIMEOUT_TOUCH_SENSOR = 0.5

def run_drum_subsystem():
    """
    Run the drum subsystem: playing is toggled by pressing the drum touch sensor.
    """
    # devices
    motor = Motor("A") # motor controlling the drum rod
    drum_touch = TouchSensor(3) # touch sensor to start/stop the drum

    # use boolean flag to track if drum is playing
    is_drum_playing = False

    while True:
        if drum_touch.is_pressed():
            is_drum_playing = not is_drum_playing

            if not is_drum_playing:
                # reset the drum to prepare for the next time it starts playing
                reset_drum(motor)

            # prevent sensor from registering multiple touches if it's being held
            time.sleep(TIMEOUT_TOUCH_SENSOR)

    if is_drum_playing:
        play_drum_bolero(motor)

def reset_drum(motor):
    """
    Resets the drum motor.
    """
    motor.set_position(ANGLE_ABSOLUTE_RESET)
    return

def play_drum_bolero(motor):
    """
    Plays the Bolero drum rhythm.
    """
    # first bar
    play_drum_eighth_note(motor, 1)
    play_drum_triplet(motor, 1)

    play_drum_eighth_note(motor, 1)
    play_drum_triplet(motor, 1)

    play_drum_eighth_note(motor, 2)

    # second bar
    play_drum_eighth_note(motor, 1)
    play_drum_triplet(motor, 1)

    play_drum_eighth_note(motor, 1)
    play_drum_triplet(motor, 2)

    return

def play_drum_triplet(motor, n_times):
    """
    Plays a triplet on the drum `n_times` number of times.
    """
    for _i in range(n_times):
        for _j in range(3):
            play_drum_note(motor, DELAY_TRIPLET)

    return

def play_drum_eighth_note(motor, n_times):
    """
    Plays an eighth note on the drum `n_times` number of times.
    """
    for _ in range(n_times):
        play_drum_note(motor, DELAY_EIGHTH_NOTE)

    return

"""
Plays a note with the specified delay once.
"""
def play_drum_note(motor, delay):
    motor.set_position_relative(-1 * ANGLE_RELATIVE_NOTE_START)
    time.sleep(delay)

    motor.set_position(ANGLE_ABSOLUTE_NOTE_END)
    time.sleep(delay)

    return