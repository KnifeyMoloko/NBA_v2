"""
Tests for the collect functions of NBA_v2
Author: Maciej Cisowski
"""

import pytest
import allure
from datetime import date
import time
import pandas as pd
from assertpy import assert_that
from app.collect import fetch_scoreboard_data


@pytest.fixture()
def define_test_dates():
    dfmt = "%Y/%m/%d"
    start = date(2019, 11, 1)
    end = date(2019, 11, 30)
    middle = date(2019, 11, 15).strftime(dfmt)
    return start, end, middle


@pytest.fixture()
def define_test_data_for_timeouts():
    dfmt = "%Y/%m/%d"
    start = date(2019, 10, 25)
    end = date(2020, 1, 5)
    middle = date(2019, 12, 6).strftime(dfmt)
    timeout_secs = 60
    timeout_days = 20
    return {"start": start,
            "end": end,
            "middle": middle,
            "timeout_days": timeout_days,
            "timeout_secs": timeout_secs}


def test_fetch_scoreboard_data_returns_dict(define_test_dates):
    assert_that(
        fetch_scoreboard_data(
            define_test_dates[0], define_test_dates[1]))\
        .is_type_of(dict)


def test_fetch_scoreboard_data_has_expected_keys(define_test_dates):
    assert_that(
        fetch_scoreboard_data(
            define_test_dates[0],
            define_test_dates[1])[define_test_dates[2]]).\
        contains("GameHeader", "LineScore", "SeriesStandings", "LastMeeting",
                 "EastConfStandingsByDay", "WestConfStandingsByDay",
                 "TeamLeaders", "Available", "TicketLinks", "WinProbability")


def test_fetch_scoreboard_data_values_are_pandas_data_frames(define_test_dates):
    check = []
    for value in fetch_scoreboard_data(
            define_test_dates[0],
            define_test_dates[1])[define_test_dates[2]].values():
        if isinstance(value, pd.DataFrame):
            check.append(value)
    assert_that(check).is_not_empty()


def test_fetch_scoreboard_waits_expected_seconds_for_intervals_of_requests(
        define_test_data_for_timeouts):
    t1 = time.time()
    fetch_scoreboard_data(start_date=define_test_data_for_timeouts["start"],
                          end_date=define_test_data_for_timeouts["end"],
                          timeout_days=define_test_data_for_timeouts["timeout_days"],
                          timeout_secs=define_test_data_for_timeouts["timeout_secs"])
    t2 = time.time()
    assert_that(t2 - t1).is_greater_than(120)


def test_fetch_scoreboard_defaults_to_config_timeout_vals(
        define_test_data_for_timeouts):
    from config import TIMEOUT_SECS
    t1 = time.time()
    fetch_scoreboard_data(start_date=define_test_data_for_timeouts["start"],
                          end_date=define_test_data_for_timeouts["end"])
    t2 = time.time()
    assert_that(t2 - t1).is_greater_than(TIMEOUT_SECS)
