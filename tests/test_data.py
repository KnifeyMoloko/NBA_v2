"""
Tests for the data manipulation functions for NBA_v2
Author: Maciej Cisowski
"""

import pytest
import allure
from datetime import date
from assertpy import assert_that
from app.collect import fetch_scoreboard_data
from app.data import merge_line_score, is_empty
from pandas import DataFrame


@pytest.fixture()
def get_test_data():
    return {
        "date": date.today().strftime("%Y/%m/%d"),
        "no_games_date": date(2019, 11, 28).strftime("%Y/%m/%d")
    }


def test_is_empty_on_date_with_no_games_returns_true(get_test_data):
    assert_that(is_empty(
        fetch_scoreboard_data(
            start_date=get_test_data["no_games_date"],
            end_date=get_test_data["no_games_date"]
        ),
        d=get_test_data["no_games_date"])).is_true()


def test_is_empty_on_date_with_games_returns_false(get_test_data):
    assert_that(is_empty(
        fetch_scoreboard_data(
            start_date=get_test_data["date"],
            end_date=get_test_data["date"]
        ), get_test_data["date"])
    )


def test_merge_line_score_on_game_returns_dict():
    assert_that(merge_line_score(fetch_scoreboard_data())).is_type_of(dict)


def test_merge_line_score_has_merged_line_score_key(get_test_data):
    assert_that(merge_line_score(
        fetch_scoreboard_data())[get_test_data.get("date")]).contains("mergedLineScore")


def test_merge_line_score_merged_line_score_is_dataframe(get_test_data):
    assert_that(
        merge_line_score(
            fetch_scoreboard_data())[get_test_data.get('date')].get(
            'mergedLineScore')
    ).is_type_of(DataFrame)


def test_merge_line_score_merged_line_score_is_half_size_of_line_score(get_test_data):
    line_score_dim_0_count = merge_line_score(
        fetch_scoreboard_data())[get_test_data.get('date')].get(
        'LineScore')["GAME_SEQUENCE"].count()

    merged_line_score_dim_0_count = merge_line_score(
        fetch_scoreboard_data())[get_test_data.get('date')].get(
        "mergedLineScore")["GAME_SEQUENCE"].count()
    assert_that(line_score_dim_0_count / merged_line_score_dim_0_count).is_equal_to(2)


def test_merged_line_score_returns_line_empty_data_frame_on_no_games_day(get_test_data):
    assert_that(merge_line_score(
        fetch_scoreboard_data(
            start_date=get_test_data["no_games_date"],
            end_date=get_test_data["no_games_date"]
        )
    )[get_test_data.get('no_games_date')].get(
            'mergedLineScore')).is_empty()
