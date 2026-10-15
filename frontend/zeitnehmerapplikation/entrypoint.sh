#!/bin/sh
set -e

replace_env() {
    var_name="$1"
    placeholder="$2"
    value=$(printenv "$var_name" || true)

    if [ -n "$value" ]; then
        escaped_value=$(printf '%s' "$value" | sed 's/[&|\\]/\\&/g')

        find /app/.next /app/public -type f \( -name "*.js" -o -name "*.html" \) \
            -exec sed -i "s|${placeholder}|${escaped_value}|g" {} +
    fi
}

replace_env NEXT_PUBLIC_DESKTOP_APP_API_URL RUNTIME_PLACEHOLDER_DESKTOP_APP_API_URL
replace_env NEXT_PUBLIC_MQTT_WORKER_API_URL RUNTIME_PLACEHOLDER_MQTT_WORKER_API_URL
replace_env NEXT_PUBLIC_API_KEY RUNTIME_PLACEHOLDER_API_KEY

exec "$@"
