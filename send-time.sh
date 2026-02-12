#!/bin/bash
BROKER="172.31.177.41"
PORT="1883"
TOPIC="esp32/timestamp"
CLIENT_ID="raspi"
ESP_ID="ESP32-$(cat /sys/class/net/wlo1/address)"

# Generate timestamp in the required format with timezone
TIMESTAMP=$(date +'%Y-%m-%dT%H:%M:%S.%6N%z')

# JSON-Payload erzeugen
PAYLOAD=$(jq -n \
    --arg esp_id "$ESP_ID" \
    --arg timestamp "$TIMESTAMP" \
    '{esp_id: $esp_id, timestamp: $timestamp}')

mosquitto_pub -h "$BROKER" -p "$PORT" -t "$TOPIC" -i "$CLIENT_ID" -m "$PAYLOAD"