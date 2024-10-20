import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the motion sensor output
MOTION_SENSOR_PIN = 27  # GPIO27 corresponds to physical pin 13

# Set up the motion sensor pin as an input
GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

print("PIR Motion Sensor Test (CTRL+C to exit)")

try:
    while True:
        if GPIO.input(MOTION_SENSOR_PIN):
            print("Motion detected!")
        else:
            print("No motion")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nTest ended by user")
finally:
    GPIO.cleanup()
