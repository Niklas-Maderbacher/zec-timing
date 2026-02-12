import threading
import sys

import paho.mqtt.client as mqtt
import json
import redis

from app.config.config import settings
from app.crud.timestamps import add_timestamp


def extract_payload(payload):
    mac_address = payload.get("esp_id")
    timestamp = payload.get("timestamp")

    # Clean values
    mac_address = mac_address.split("-", 1)[1]

    add_timestamp(mac_address, timestamp)

    return mac_address, timestamp

def on_connect(client, userdata, flags, rc):
    print(f"Connect with result code {rc}")

def on_message(client, userdata, msg):
    try:
        mac, timestamp = extract_payload(json.loads(msg.payload.decode("utf-8")))
        print(f"Received mac-address: {mac} and timestamp: {timestamp}")
    except json.JSONDecodeError:
        print("Received message is not valid JSON", file=sys.stdout)

def run_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(settings.MQTT_IP, settings.MQTT_PORT)
    client.subscribe(settings.MQTT_TOPIC)

    client.loop_forever()

def start_mqtt_worker():
    thread = threading.Thread(target=run_client, daemon=True)
    thread.start()
    print("[MQTT] Worker thread started")