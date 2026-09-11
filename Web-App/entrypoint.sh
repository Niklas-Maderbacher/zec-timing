#!/bin/sh

set -e

cat <<EOF > /app/public/env.js
window.__ENV__ = {
  API_URL: "${NEXT_PUBLIC_API_URL}"
};
EOF

exec "$@"