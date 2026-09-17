import pytest

from app.crud.timestamps import add_timestamp, get_timestamps, delete_timestamps
from app.exceptions.mac_not_found import MacNotFound


def test_calls_zadd_with_namespaced_key(mock_redis, frozen_time, fixed_expire):
    add_timestamp("AA:BB:CC:DD:EE:FF", "2025-10-12T15:30:00")

    args, _ = mock_redis.zadd.call_args
    key = args[0]
    assert key == "timestamps:AA:BB:CC:DD:EE:FF"

def test_score_is_now_plus_expire_time(mock_redis, frozen_time, fixed_expire):
    add_timestamp("AA:BB:CC:DD:EE:FF", "2025-10-12T15:30:00")

    mock_redis.zadd.assert_called_once_with(
        "timestamps:AA:BB:CC:DD:EE:FF",
        {"2025-10-12T15:30:00": 1_000_000.0 + 3600},
    )

def test_uses_current_expire_setting(mock_redis, frozen_time, monkeypatch):
    monkeypatch.setattr("app.crud.timestamps.settings.TIMESTAMP_EXPIRE_TIME", 60)

    add_timestamp("AA:BB:CC:DD:EE:FF", "some-timestamp")

    args = mock_redis.zadd.call_args[0]
    assert args[1] == {"some-timestamp": 1_000_000.0 + 60}

def test_does_not_raise_when_key_already_has_entries(mock_redis, frozen_time, fixed_expire):
    mock_redis.zadd.return_value = 0  # redis returns 0 when updating an existing member
    add_timestamp("AA:BB:CC:DD:EE:FF", "2025-10-12T15:30:00")  # should not raise


def test_trims_expired_entries_before_checking_existence(mock_redis, frozen_time):
    mock_redis.exists.return_value = True
    mock_redis.zrange.return_value = []

    get_timestamps("AA:BB:CC:DD:EE:FF")

    mock_redis.zremrangebyscore.assert_called_once_with(
        "timestamps:AA:BB:CC:DD:EE:FF", 0, 1_000_000.0
    )
    # trimming must happen before the existence check
    call_order = [c[0] for c in mock_redis.method_calls]
    assert call_order.index("zremrangebyscore") < call_order.index("exists")

def test_raises_mac_not_found_when_key_absent(mock_redis, frozen_time):
    mock_redis.exists.return_value = False

    with pytest.raises(MacNotFound):
        get_timestamps("AA:BB:CC:DD:EE:FF")

    mock_redis.zrange.assert_not_called()

def test_returns_zrange_result_when_key_present(mock_redis, frozen_time):
    mock_redis.exists.return_value = True
    mock_redis.zrange.return_value = ["2025-10-12T15:30:00", "2025-10-12T16:00:00"]

    result = get_timestamps("AA:BB:CC:DD:EE:FF")

    assert result == ["2025-10-12T15:30:00", "2025-10-12T16:00:00"]
    mock_redis.zrange.assert_called_once_with(
        "timestamps:AA:BB:CC:DD:EE:FF", 0, -1
    )

def test_uses_namespaced_key_consistently(mock_redis, frozen_time):
    mock_redis.exists.return_value = True
    mock_redis.zrange.return_value = []

    get_timestamps("11:22:33:44:55:66")

    expected_key = "timestamps:11:22:33:44:55:66"
    assert mock_redis.zremrangebyscore.call_args[0][0] == expected_key
    assert mock_redis.exists.call_args[0][0] == expected_key
    assert mock_redis.zrange.call_args[0][0] == expected_key

def test_deletes_key_when_present(mock_redis):
    mock_redis.exists.return_value = True

    delete_timestamps("AA:BB:CC:DD:EE:FF")

    mock_redis.delete.assert_called_once_with("timestamps:AA:BB:CC:DD:EE:FF")

def test_returns_none(mock_redis):
    mock_redis.exists.return_value = True

    result = delete_timestamps("AA:BB:CC:DD:EE:FF")

    assert result is None