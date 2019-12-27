"""
Tests for the collect functions of NBA_v2
Author: Maciej Cisowski
"""

import pytest
import allure
import pandas as pd
from assertpy import assert_that
from app.collect import fetch_scoreboard_data


def test_fetch_scoreboard_data_returns_dict():
    assert_that(fetch_scoreboard_data()).is_type_of(dict)


def test_fetch_scoreboard_data_has_expected_keys():
    assert_that(fetch_scoreboard_data().keys()).contains(
        "LineScore",
         "SeriesStandings",
         "EastConfStandingsByDay",
         "WestConfStandingsByDay"
    )


def test_fetch_scoreboard_data_values_are_pandas_data_frames():
    check = []
    for value in fetch_scoreboard_data().values():
        print(isinstance(value, pd.DataFrame))
        if isinstance(value, pd.DataFrame):
            check.append(value)
    assert check
