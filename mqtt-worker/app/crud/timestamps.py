from app.config.config import settings
from app.redis.redis import redis_connection, redis_lock
from app.exceptions.mac_not_found import MacNotFound

def add_timestamp(mac: str, timestamp: str):
    with redis_lock:
        # Store data in Redis list
        redis_connection.rpush(mac, timestamp)


def get_timestamps(mac: str):
    with redis_lock:

        # Check if the key exists in Redis
        if not redis_connection.exists(mac):
            raise MacNotFound(
                message=("No ESP with this MAC address exists or no timestamps yet exist. "
                    "If you think it should exist, please send new MQTT data."),
                error_code=404
            )

        # Only get newest timestamp
        return redis_connection.lrange(mac, 0, -1)

def delete_timestamps(mac: str):
    with redis_lock:
        # Check if the key exists
        if not redis_connection.exists(mac):
            raise MacNotFound(
                message=("No ESP with this MAC address exists or no timestamps yet exist. "
                    "If you think it should exist, please send new MQTT data."),
                error_code=404
            )

        # Delete all timestamps for this MAC
        return redis_connection.ltrim(mac, 0, 0)