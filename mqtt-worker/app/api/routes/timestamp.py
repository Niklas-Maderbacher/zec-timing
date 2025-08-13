from fastapi import APIRouter, HTTPException, status

from app.mqtt.pull_timestamps import messages
from app.schemas.timestamp import Timestamp


router = APIRouter(prefix="/timestamps", tags=["Timestamps"])

@router.get("/{esp_mac}", response_model=Timestamp)
def get_timestamp_from_esp(esp_mac: str):
    if esp_mac.replace("-", ":") in messages:
        return Timestamp(timestamp=messages[esp_mac.replace("-", ":")])
    else:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No esp with this mac-address exists or no timestamp yet exsists." +
                "If you think an esp with this timestamp does exists," +
                "please provide a timestamp so that the list can be updated"
            )


@router.delete("/{esp_mac}")
def reset_esp_timestamps(esp_mac: str):
    if esp_mac.replace("-", ":") in messages:
        messages[esp_mac.replace("-", ":")].clear()
        return True
    else:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No esp with this mac-address exists or no timestamp yet exsists." +
                "If you think an esp with this timestamp does exists," +
                "please provide a timestamp so that the list can be updated"
            )
