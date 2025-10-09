#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick
from time import sleep


COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"


# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(3) # Port S3
TOUCH_SENSOR = TouchSensor(1) # Port S1

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data():
    "Collect color sensor data."
    output = open(COLOR_SENSOR_DATA_FILE, "a") # open the csv file in append mode to not overwrite old data
    try: 
        counter = 0
        while True:
            if TOUCH_SENSOR.is_pressed():
                color_data = COLOR_SENSOR.get_rgb() # get the RGB values from color sensor
                if color_data is not None and color_data[0] is not None: # pass if the collection failed (if None)
                    counter += 1
                    print(f"Data point #{counter}: {color_data}") # print to terminal for user
                    output.write(f"{color_data}\n") # write color data to file
                else:
                    print("Failed: color data was none")
                sleep(0.5) # so only collect one data point per button press
    except KeyboardInterrupt:
        print("Finished collecting RGB data.")
    except BaseException:
        pass
    finally:
        output.close()
        reset_brick() # turn off everything on the brick's hardware, and reset it
        exit()



if __name__ == "__main__":
    collect_color_sensor_data()
