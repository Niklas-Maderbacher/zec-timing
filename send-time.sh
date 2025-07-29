#!/bin/bash

BROKER="192.168.1.111"
PORT="1883"
TOPIC="time"
CLIENT_ID="raspi"

CURRENT_DATE=$(date +"%H:%M:%S.%6N")

mosquitto_pub -h "$BROKER" -p "$PORT" -t "$TOPIC" -i "$CLIENT_ID" -m "$CURRENT_DATE"

