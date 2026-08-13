import pandas as pd
import pytest

from analytics import (
    load_events,
    get_connection,
    total_signups,
    activation_funnel,
    activation_rate,
    daily_active_users,
)


@pytest.fixture
def sample_df():
    """A small, deterministic events table independent of data/events.csv,
    so these tests don't break if the sample data file changes."""
    return pd.DataFrame([
        {"user_id": 1, "event": "signup", "timestamp": "2025-01-01 09:00:00"},
        {"user_id": 1, "event": "create_project", "timestamp": "2025-01-01 09:05:00"},
        {"user_id": 2, "event": "signup", "timestamp": "2025-01-01 10:00:00"},
        {"user_id": 3, "event": "signup", "timestamp": "2025-01-02 08:00:00"},
        {"user_id": 3, "event": "create_project", "timestamp": "2025-01-02 08:10:00"},
    ])


@pytest.fixture
def con(sample_df):
    return get_connection(sample_df)


def test_total_signups(con):
    assert total_signups(con) == 3


def test_activation_funnel_counts(con):
    funnel = activation_funnel(con)
    assert funnel["signups"] == 3
    assert funnel["created_project"] == 2
    assert funnel["invited_teammates"] == 0


def test_activation_rate(con):
    assert activation_rate(con) == pytest.approx(2 / 3)


def test_activation_rate_handles_zero_signups():
    empty_events = pd.DataFrame([
        {"user_id": 1, "event": "view_dashboard", "timestamp": "2025-01-01 09:00:00"},
    ])
    con = get_connection(empty_events)
    assert activation_rate(con) == 0.0


def test_daily_active_users_shape(con):
    dau = daily_active_users(con)
    assert list(dau.columns) == ["day", "daily_active_users"]
    assert dau["daily_active_users"].sum() == 3


def test_load_events_rejects_missing_columns(tmp_path):
    bad_csv = tmp_path / "bad_events.csv"
    bad_csv.write_text("user_id,event\n1,signup\n")
    with pytest.raises(ValueError, match="missing required column"):
        load_events(str(bad_csv))


def test_load_events_rejects_empty_file(tmp_path):
    empty_csv = tmp_path / "empty_events.csv"
    empty_csv.write_text("user_id,event,timestamp\n")
    with pytest.raises(ValueError, match="no rows"):
        load_events(str(empty_csv))
