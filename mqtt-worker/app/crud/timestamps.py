import time

from app.config.config import settings
from app.redis.redis import redis_connection
from app.exceptions.mac_not_found import MacNotFound



def add_timestamp(mac: str, timestamp: str):
    key = f"timestamps:{mac}"
    expires_at = time.time() + settings.TIMESTAMP_EXPIRE_TIME

    redis_connection.zadd(
        key,
        {timestamp: expires_at}
    )


def get_timestamps(mac: str):
    key = f"timestamps:{mac}"
    now = time.time()

    # Remove timestamps that have expired
    redis_connection.zremrangebyscore(key, 0, now)

    if not redis_connection.exists(key):
        raise MacNotFound(
            message=(
                "No ESP with this MAC address exists or no timestamps yet exist. "
                "If you think it should exist, please send new MQTT data."
            ),
            error_code=404,
        )

    return redis_connection.zrange(key, 0, -1)


def delete_timestamps(mac: str):
    key = f"timestamps:{mac}"

    if not redis_connection.exists(key):
        raise MacNotFound(
            message=(
                "No ESP with this MAC address exists or no timestamps yet exist. "
                "If you think it should exist, please send new MQTT data."
            ),
            error_code=404,
        )

    redis_connection.delete(key)
