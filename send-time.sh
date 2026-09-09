#!/bin/bash

BROKER="192.168.1.113"
PORT="1883"
TOPIC="esp32/timestamp"
CLIENT_ID="raspi"

MQTT_USER="zecuser"
MQTT_PASSWORD="supersecret"

ESP_ID="ESP32-$(cat /sys/class/net/wlo1/address)"

# Generate timestamp in the required format with timezone
TIMESTAMP=$(date +'%Y-%m-%dT%H:%M:%S.%6N%z')

# Generate JSON payload
PAYLOAD=$(jq -n \
    --arg esp_id "$ESP_ID" \
    --arg timestamp "$TIMESTAMP" \
    '{esp_id: $esp_id, timestamp: $timestamp}')

# Publish timestamp to MQTT broker
mosquitto_pub \
    -h "$BROKER" \
    -p "$PORT" \
    -t "$TOPIC" \
    -i "$CLIENT_ID" \
    -u "$MQTT_USER" \
    -P "$MQTT_PASSWORD" \
    -m "$PAYLOAD"
