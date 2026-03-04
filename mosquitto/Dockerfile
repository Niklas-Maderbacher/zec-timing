FROM eclipse-mosquitto:latest

# Install required tools
RUN apk add --no-cache bash

# Copy entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Copy default mosquitto config
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
