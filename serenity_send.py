from sense_hat import SenseHat
from time import sleep
import requests

sense = SenseHat()

TEMP_OFFSET = 21.0

GREEN = (0, 255, 0)
AMBER = (255, 165, 0)
RED = (255, 0, 0)

API_URL = "http://192.168.0.12/serenity-api/add_reading.php"

def get_corrected_temp():
    raw_temp = sense.get_temperature()
    corrected_temp = raw_temp - TEMP_OFFSET
    return raw_temp, corrected_temp

def get_status(temp):
    if 18 <= temp <= 24:
        return "Comfortable"
    elif 24 < temp <= 26:
        return "Warning"
    else:
        return "Uncomfortable"

def show_status(status):
    if status == "Comfortable":
        sense.clear(*GREEN)
    elif status == "Warning":
        sense.clear(*AMBER)
    else:
        sense.clear(*RED)

while True:
    raw_temp, corrected_temp = get_corrected_temp()
    humidity = sense.get_humidity()
    status = get_status(corrected_temp)

    print(
        f"Raw Temp: {raw_temp:.2f} C | "
        f"Corrected Temp: {corrected_temp:.2f} C | "
        f"Humidity: {humidity:.2f}% | "
        f"Status: {status}"
    )

    show_status(status)

    data = {
        "raw_temp": round(raw_temp, 2),
        "corrected_temp": round(corrected_temp, 2),
        "humidity": round(humidity, 2),
        "status": status
    }

    try:
        response = requests.post(API_URL, data=data, timeout=10)
        print("Server response:", response.text)
    except Exception as e:
        print("Error sending data:", e)

    sleep(10)
