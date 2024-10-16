import time
import board
import adafruit_dht
import json
import os
from datetime import datetime

# + to pin 2 (5v)
# - to pin 6 (gnd)
# data to pin 7

# Define the sensor type (DHT22) and the pin it's connected to
DHT_PIN = (
    board.D4
)  # This is GPIO4, which corresponds to physical pin 7 on Raspberry Pi 3B

# Initialize the DHT device
dht = adafruit_dht.DHT22(DHT_PIN)

print("DHT22 Test Program")
print("Press Ctrl+C to exit")

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

try:
    while True:
        try:
            # Read humidity and temperature
            humidity = dht.humidity
            temperature = dht.temperature

            if humidity is not None and temperature is not None:
                print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")

                # Create a dictionary with the sensor data
                sensor_data = {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "temperature": round(temperature, 1),
                    "humidity": round(humidity, 1),
                }

                # Write the data to a JSON file
                with open("data/data_sensor.json", "w") as f:
                    json.dump(sensor_data, f, indent=4)
            else:
                print("Failed to retrieve data from DHT22 sensor")

        except RuntimeError as e:
            # DHT22 sensors are sensitive, errors are common. We'll just print the error and try again.
            print(f"Reading error: {e.args[0]}")

        time.sleep(1)  # Wait for 1 second before the next reading

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    dht.exit()
