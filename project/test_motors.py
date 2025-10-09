from utils.brick import Motor
import time

motor = Motor("A")
motor.set_position(4)
time.sleep(1)

# motor.reset_encoder()

ANGLE = 25
DELAY = 0.10

i = 0
while i < 20:
	motor.set_position_relative(-1 * ANGLE) # 100%
	time.sleep(DELAY)
	motor.set_position(11)
	# motor.set_position_relative(ANGLE) # 100%
	time.sleep(DELAY)
	i += 1
motor.set_position(4)

# motor.set_power(15) # 100%
# time.sleep(0.2)
# motor.set_power(-15) # 100%
# time.sleep(0.2)
# motor.set_power(100) # 100%
# motor.set_power(-50) # Backwards 50%
# motor.set_power(0)   # Stops motor. Motor cannot rotate.

# motor.set_power(100) # 100%
# motor.set_dps(20)
# motor.set_dps(-720) # Backwards 720 deg/sec
# motor.set_dps(0)
