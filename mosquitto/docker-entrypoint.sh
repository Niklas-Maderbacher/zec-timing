#!/bin/bash
set -e

# Use env vars or fall back to defaults
MQTT_USER="${MQTT_USER:-admin}"
MQTT_PASSWORD="${MQTT_PASSWORD:-password}"

echo "Creating MQTT user: $MQTT_USER"

# Create password file with the given credentials
mosquitto_passwd -c -b /mosquitto/config/passwd "$MQTT_USER" "$MQTT_PASSWORD"

# Execute the main command (mosquitto)
exec "$@"