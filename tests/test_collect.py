"""
Tests for the collect functions of NBA_v2
Author: Maciej Cisowski
"""

import pytest
import allure
from datetime import date
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
