#!/bin/sh
set -e

replace_env() {
  var_name="$1"
  placeholder="$2"
  value=$(eval echo "\$$var_name")
  if [ -n "$value" ]; then
    find /app/.next /app/public -type f \( -name "*.js" -o -name "*.html" \) \
      -exec sed -i "s|${placeholder}|${value}|g" {} +
  fi
}

replace_env NEXT_PUBLIC_API_URL RUNTIME_PLACEHOLDER_API_URL

exec "$@"