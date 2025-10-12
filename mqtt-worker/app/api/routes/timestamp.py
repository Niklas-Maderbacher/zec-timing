from fastapi import APIRouter, HTTPException, status

from app.schemas.timestamp import Timestamp
from app.redis.redis import redis_connection, redis_lock


router = APIRouter(prefix="/timestamps", tags=["Timestamps"])

@router.get("/{esp_mac}", response_model=Timestamp)
def get_timestamp_from_esp(esp_mac: str):
    clean_mac = esp_mac.replace("-", ":")

    with redis_lock:

        # Check if the key exists in Redis
        if not redis_connection.exists(clean_mac):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "No ESP with this MAC address exists or no timestamps yet exist. "
                    "If you think it should exist, please send new MQTT data."
                )
            )

        # Only get newest timestamp
        timestamps = redis_connection.lrange(clean_mac, -1, -1)

    return Timestamp(timestamp=timestamps)


@router.delete("/{esp_mac}")
def reset_esp_timestamps(esp_mac: str):
    # Normalize MAC (AA-BB-CC → AA:BB:CC)
    clean_mac = esp_mac.replace("-", ":")

    with redis_lock:
        # Check if the key exists
        if not redis_connection.exists(clean_mac):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "No ESP with this MAC address exists or no timestamps yet exist. "
                    "If you think an ESP with this MAC does exist, please send new data via MQTT."
                )
            )

        # Delete all timestamps for this MAC
        redis_connection.ltrim(clean_mac, 1, 0)

    return {"message": f"All timestamps deleted for {clean_mac}"}
