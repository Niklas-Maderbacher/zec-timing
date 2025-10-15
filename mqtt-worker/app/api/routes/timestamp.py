from fastapi import APIRouter, status, HTTPException

from app.schemas.timestamp import Timestamp
from app.crud.timestamps import get_timestamps, delete_timestamps
from app.exceptions.mac_not_found import MacNotFound


router = APIRouter(prefix="/timestamps", tags=["Timestamps"])

@router.get("/{esp_mac}", response_model=Timestamp, status_code=status.HTTP_200_OK)
def get_timestamp_from_esp(esp_mac: str):
    clean_mac = esp_mac.replace("-", ":")
    try:
        timestamps = get_timestamps(clean_mac)
    except MacNotFound as e:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "No ESP with this MAC address exists or no timestamps yet exist. "
                    "If you think it should exist, please send new MQTT data."
                )
            )

    return Timestamp(timestamp=timestamps)


@router.delete("/{esp_mac}", response_model=Timestamp, status_code=status.HTTP_202_ACCEPTED)
def reset_esp_timestamps(esp_mac: str):
    clean_mac = esp_mac.replace("-", ":")

    timestamps = delete_timestamps(clean_mac)

    return Timestamp(timestamp=timestamps)
