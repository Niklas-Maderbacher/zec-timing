import pytest
import json

from app.mqtt.pull_timestamps import extract_payload

# Sample payload
payload = {
    "esp_id": "ESP-ABCD1234",
    "timestamp": "2025-10-12T15:30:00"
}


def test_extract_payload_returns_cleaned_values(mock_redis, mock_lock):
    payload = {"esp_id": "ESP-ABCD1234", "timestamp": "2025-10-12T15:30:00"}
    mac, ts = extract_payload(payload)
    assert mac == "ABCD1234"
    assert ts == "15:30:00"
    mock_redis.rpush.assert_called_once_with("ABCD1234", "15:30:00")

def test_extract_payload_mac_with_extra_dash(mock_redis, mock_lock):
    payload = {"esp_id": "ESP-12-34-56", "timestamp": "2025-10-12T09:45:10"}
    mac, ts = extract_payload(payload)
    assert mac == "12-34-56"
    assert ts == "09:45:10"
    mock_redis.rpush.assert_called_once_with("12-34-56", "09:45:10")

def test_extract_payload_timestamp_with_ms(mock_redis, mock_lock):
    payload = {"esp_id": "ESP-XYZ", "timestamp": "2025-10-12T23:59:59.123"}
    mac, ts = extract_payload(payload)
    assert mac == "XYZ"
    assert ts == "23:59:59.123"
    mock_redis.rpush.assert_called_once_with("XYZ", "23:59:59.123")

def test_extract_payload_missing_esp_id(mock_redis, mock_lock):
    payload = {"timestamp": "2025-10-12T15:30:00"}
    with pytest.raises(AttributeError):
        extract_payload(payload)  # mac_address is None → split() fails

def test_extract_payload_missing_timestamp(mock_redis, mock_lock):
    payload = {"esp_id": "ESP-ABCD"}
    with pytest.raises(AttributeError):
        extract_payload(payload)  # timestamp is None → split() fails

def test_extract_payload_empty_payload(mock_redis, mock_lock):
    payload = {}
    with pytest.raises(AttributeError):
        extract_payload(payload)
