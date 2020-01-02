"""
Tests for the commit functions of NBA_v2
Author: Maciej Cisowski
"""

import pytest
import allure
from assertpy import assert_that
from sqlalchemy.engine import Connection
from datetime import date
from app.commit import start_engine
from app.collect import fetch_scoreboard_data


@pytest.fixture()
def get_data_frame():
    dfmt = "%Y/%m/%d"
    start = date(2019, 12, 1)
    end = date(2019, 12, 3)
    middle = date(2019, 12, 2).strftime(dfmt)
    return fetch_scoreboard_data(start_date=start,
                                 end_date=end)[middle]


@pytest.fixture()
def get_engine():
    return start_engine()


def test_connection_for_local_dev_db(get_engine):
    assert_that(get_engine.connect()).is_type_of(Connection)


def test_committing_to_a_new_db_creates_new_db_and_table(get_engine, get_data_frame):
    db = get_engine
    df = get_data_frame["LineScore"]
    df.to_sql("test_table", con=db)
    assert_that(db.execute("SELECT * FROM test_table").fetchall()).is_not_empty()
