import pytest

from app.exceptions.mac_not_found import MacNotFound


def test_get_returns_200_and_timestamp_on_success(client, mock_get_timestamps):
    mock_get_timestamps.return_value = ["2025-10-12T15:30:00"]

    response = client.get("/timestamps/AA:BB:CC:DD:EE:FF")

    assert response.status_code == 200
    assert response.json() == {"timestamp": ["2025-10-12T15:30:00"]}
    mock_get_timestamps.assert_called_once_with("AA:BB:CC:DD:EE:FF")


def test_get_converts_dashes_to_colons_in_mac(client, mock_get_timestamps):
    mock_get_timestamps.return_value = []

    client.get("/timestamps/AA-BB-CC-DD-EE-FF")

    mock_get_timestamps.assert_called_once_with("AA:BB:CC:DD:EE:FF")


def test_get_passes_mac_unchanged_when_already_colon_separated(client, mock_get_timestamps):
    mock_get_timestamps.return_value = []

    client.get("/timestamps/11:22:33:44:55:66")

    mock_get_timestamps.assert_called_once_with("11:22:33:44:55:66")


def test_get_returns_404_when_mac_not_found(client, mock_get_timestamps):
    mock_get_timestamps.side_effect = MacNotFound(message="not found", error_code=404)

    response = client.get("/timestamps/AA:BB:CC:DD:EE:FF")

    assert response.status_code == 404
    assert "No ESP with this MAC address exists" in response.json()["detail"]


def test_get_returns_empty_list_when_no_timestamps_yet(client, mock_get_timestamps):
    mock_get_timestamps.return_value = []

    response = client.get("/timestamps/AA:BB:CC:DD:EE:FF")

    assert response.status_code == 200
    assert response.json() == {"timestamp": []}


def test_delete_returns_202_and_timestamp_on_success(client, mock_delete_timestamps):
    mock_delete_timestamps.return_value = None

    response = client.delete("/timestamps/AA:BB:CC:DD:EE:FF")

    assert response.status_code == 202
    mock_delete_timestamps.assert_called_once_with("AA:BB:CC:DD:EE:FF")


def test_delete_converts_dashes_to_colons_in_mac(client, mock_delete_timestamps):
    mock_delete_timestamps.return_value = None

    client.delete("/timestamps/AA-BB-CC-DD-EE-FF")

    mock_delete_timestamps.assert_called_once_with("AA:BB:CC:DD:EE:FF")


def test_delete_mac_not_found_is_unhandled_and_propagates(client, mock_delete_timestamps):
    mock_delete_timestamps.side_effect = MacNotFound(message="not found", error_code=404)

    with pytest.raises(MacNotFound):
        client.delete("/timestamps/AA:BB:CC:DD:EE:FF")