#!/bin/bash
set -e

MQTT_USER="${MQTT_USER:-admin}"
MQTT_PASSWORD="${MQTT_PASSWORD:-password}"

echo "Creating MQTT user: $MQTT_USER"

mosquitto_passwd -c -b /mosquitto/config/passwd "$MQTT_USER" "$MQTT_PASSWORD"
chown mosquitto:mosquitto /mosquitto/config/passwd
chmod 600 /mosquitto/config/passwd

exec "$@"
