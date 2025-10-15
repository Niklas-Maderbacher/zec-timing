#!/bin/bash

BROKER="172.31.183.187"
PORT="1883"
TOPIC="esp32/timestamp"
CLIENT_ID="raspi"

ESP_ID="ESP32-$(cat /sys/class/net/wlo1/address)"
TIMESTAMP=$(date +"%Y-%m-%dT%H:%M:%S.%6N")

# JSON-Payload erzeugen
PAYLOAD=$(jq -n \
  --arg esp_id "$ESP_ID" \
  --arg timestamp "$TIMESTAMP" \
  '{esp_id: $esp_id, timestamp: $timestamp}')

mosquitto_pub -h "$BROKER" -p "$PORT" -t "$TOPIC" -i "$CLIENT_ID" -m "$PAYLOAD"
