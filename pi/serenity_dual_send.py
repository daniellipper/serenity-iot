from time import sleep
import json
import requests
import paho.mqtt.client as mqtt
from sense_hat import SenseHat

# =========================
# CONFIG
# =========================
API_URL = "http://192.168.0.12/serenity-api/add_reading.php"
CONTROL_URL = "http://192.168.0.12/serenity-api/control.php"

DEVICE_ID = "Mq91baGxCeHpVEDs5sRadide"
DEVICE_TOKEN = "4wbH804YBeYJfgY7Pw8DcR3mG6LHcUGaGNxVP2wI"
MQTT_BROKER = "api.allthingstalk.io"
MQTT_PORT = 1883

TEMP_OFFSET = 22.0
SEND_INTERVAL = 10  # seconds

GREEN = (0, 255, 0)
AMBER = (255, 165, 0)
RED = (255, 0, 0)

# =========================
# SETUP
# =========================
sense = SenseHat()


def on_connect(client, userdata, flags, rc, properties=None):
    print("MQTT connect rc =", rc)


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set(f"maker:{DEVICE_TOKEN}", "")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()


# =========================
# HELPERS
# =========================
def get_corrected_temp():
    raw_temp = sense.get_temperature()
    corrected_temp = raw_temp - TEMP_OFFSET
    return raw_temp, corrected_temp


def get_humidity():
    return sense.get_humidity()


def get_status(corrected_temp):
    if 18 <= corrected_temp <= 24:
        return "Comfortable"
    elif 24 < corrected_temp <= 26:
        return "Warning"
    else:
        return "Uncomfortable"


def get_status_code(status):
    if status == "Comfortable":
        return 0
    elif status == "Warning":
        return 1
    else:
        return 2


def show_status_on_matrix(status):
    if status == "Comfortable":
        sense.clear(*GREEN)
    elif status == "Warning":
        sense.clear(*AMBER)
    else:
        sense.clear(*RED)


def clear_matrix():
    sense.clear()


def get_alert_state():
    try:
        response = requests.get(CONTROL_URL, timeout=5)
        data = response.json()
        if data.get("success"):
            return int(data.get("alert_enabled", 1))
    except Exception as e:
        print("Error getting alert state:", e)
    return 1


def send_to_php(raw_temp, corrected_temp, humidity, status):
    payload = {
        "raw_temp": round(raw_temp, 2),
        "corrected_temp": round(corrected_temp, 2),
        "humidity": round(humidity, 2),
        "status": status
    }

    response = requests.post(API_URL, data=payload, timeout=10)
    print("PHP response:", response.text)


def send_to_allthingstalk(corrected_temp, humidity, status_code):
    mqtt_client.publish(
        f"device/{DEVICE_ID}/asset/temperature/state",
        json.dumps({"value": round(corrected_temp, 2)})
    )
    mqtt_client.publish(
        f"device/{DEVICE_ID}/asset/humidity/state",
        json.dumps({"value": round(humidity, 2)})
    )
    mqtt_client.publish(
        f"device/{DEVICE_ID}/asset/status_code/state",
        json.dumps({"value": status_code})
    )
    print("Sent to AllThingsTalk")


# =========================
# MAIN LOOP
# =========================
try:
    while True:
        raw_temp, corrected_temp = get_corrected_temp()
        humidity = get_humidity()

        status = get_status(corrected_temp)
        status_code = get_status_code(status)
        alert_enabled = get_alert_state()

        print(
            f"Raw Temp: {raw_temp:.2f} C | "
            f"Corrected Temp: {corrected_temp:.2f} C | "
            f"Humidity: {humidity:.2f}% | "
            f"Status: {status} | "
            f"Alert Enabled: {alert_enabled}"
        )

        if alert_enabled == 1:
            show_status_on_matrix(status)
        else:
            clear_matrix()

        try:
            send_to_php(raw_temp, corrected_temp, humidity, status)
        except Exception as e:
            print("Error sending to PHP API:", e)

        try:
            send_to_allthingstalk(corrected_temp, humidity, status_code)
        except Exception as e:
            print("Error sending to AllThingsTalk:", e)

        sleep(SEND_INTERVAL)

except KeyboardInterrupt:
    print("\nStopping Serenity...")
    clear_matrix()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
