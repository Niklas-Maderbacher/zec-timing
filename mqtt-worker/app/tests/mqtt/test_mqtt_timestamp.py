import pytest

from app.mqtt.pull_timestamps import extract_payload


class TestExtractPayload:
    def test_returns_mac_and_timestamp_unchanged(self, mock_add_timestamp):
        payload = {"esp_id": "ESP-ABCD1234", "timestamp": "2025-10-12T15:30:00"}

        mac, ts = extract_payload(payload)

        assert mac == "ABCD1234"
        assert ts == "2025-10-12T15:30:00"
        mock_add_timestamp.assert_called_once_with("ABCD1234", "2025-10-12T15:30:00")

    def test_mac_with_extra_dashes_only_splits_on_first(self, mock_add_timestamp):
        payload = {"esp_id": "ESP-12-34-56", "timestamp": "2025-10-12T09:45:10"}

        mac, ts = extract_payload(payload)

        assert mac == "12-34-56"
        assert ts == "2025-10-12T09:45:10"
        mock_add_timestamp.assert_called_once_with("12-34-56", "2025-10-12T09:45:10")

    def test_timestamp_with_milliseconds_passes_through(self, mock_add_timestamp):
        payload = {"esp_id": "ESP-XYZ", "timestamp": "2025-10-12T23:59:59.123"}

        mac, ts = extract_payload(payload)

        assert mac == "XYZ"
        assert ts == "2025-10-12T23:59:59.123"
        mock_add_timestamp.assert_called_once_with("XYZ", "2025-10-12T23:59:59.123")

    def test_missing_esp_id_raises_attribute_error(self, mock_add_timestamp):
        payload = {"timestamp": "2025-10-12T15:30:00"}

        with pytest.raises(AttributeError):
            extract_payload(payload)

        mock_add_timestamp.assert_not_called()

    def test_missing_timestamp_is_forwarded_as_none(self, mock_add_timestamp):
        payload = {"esp_id": "ESP-ABCD"}

        mac, ts = extract_payload(payload)

        assert mac == "ABCD"
        assert ts is None
        mock_add_timestamp.assert_called_once_with("ABCD", None)

    def test_empty_payload_raises_attribute_error(self, mock_add_timestamp):
        payload = {}

        with pytest.raises(AttributeError):
            extract_payload(payload)

        mock_add_timestamp.assert_not_called()

    def test_esp_id_without_dash_raises_index_error(self, mock_add_timestamp):
        payload = {"esp_id": "ABCD1234", "timestamp": "2025-10-12T15:30:00"}

        with pytest.raises(IndexError):
            extract_payload(payload)

        mock_add_timestamp.assert_not_called()