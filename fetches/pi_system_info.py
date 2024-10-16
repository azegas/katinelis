import psutil
from gpiozero import CPUTemperature
import json
from datetime import datetime
import os
import time
import sys
from dotenv import load_dotenv

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log_config import logger

load_dotenv()

def fetch_and_save_raspberry_system_info():
    logger.info("##########################################################")
    logger.info("Fetch raspberry system info START")

    # Get system info
    cpu = psutil.cpu_percent(interval=1)  # Get CPU usage over 1 second
    memory = psutil.virtual_memory().percent
    temp = CPUTemperature().temperature
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate uptime
    seconds = time.monotonic()
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if days == 1:
        uptime = f"1 day and {int(hours)}:{int(minutes):02d} hours"
    elif days > 1:
        uptime = f"{int(days)} days and {int(hours)}:{int(minutes):02d} hours"
    else:
        if hours == 0:
            uptime = f"{int(minutes):02d}"
        else:
            uptime = f"{int(hours)}:{int(minutes):02d}"
    
    info = {
        "timestamp": date,
        "cpu_usage": cpu,
        "memory_usage": memory,
        "temperature": temp,
        "uptime": uptime
    }

    # Save to file
    base_dir = os.getenv("BASE_DIR")
    file_path = os.path.join(base_dir, "data/system_info.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(info, f, indent=4)
    logger.info(f"Data saved to {file_path}")

    # Verify the file was updated
    with open(file_path, "r") as f:
        saved_data = json.load(f)
    logger.info("Saved data: %s", saved_data)
    logger.info("System info fetched and saved")

    logger.info("Fetch raspberry system info END")
    logger.info("##########################################################")

if __name__ == "__main__":
    fetch_and_save_raspberry_system_info()