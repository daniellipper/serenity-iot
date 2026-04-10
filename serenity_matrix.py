from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

TEMP_OFFSET = 21.0

GREEN = (0, 255, 0)
AMBER = (255, 165, 0)
RED = (255, 0, 0)

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
    humidity = sense.get_humidity()  # optional

    status = get_status(corrected_temp)

    print(
        f"Raw Temp: {raw_temp:.2f} C | "
        f"Corrected Temp: {corrected_temp:.2f} C | "
        f"Humidity: {humidity:.2f}% | "
        f"Status: {status}"
    )

    show_status(status)
    sleep(5)
