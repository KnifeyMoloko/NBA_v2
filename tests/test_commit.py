"""
Tests for the commit functions of NBA_v2
Author: Maciej Cisowski
"""

import pytest
import allure
from assertpy import assert_that
from sqlalchemy.engine import Connection
from datetime import date
#from app.commit import *
from app.collect import fetch_scoreboard_data


@pytest.fixture()
def get_data_frame():
    dfmt = "%Y/%m/%d"
    start = date(2019, 12, 1)
    end = date(2019, 12, 30)
    middle = date(2019, 12, 15).strftime(dfmt)
    return fetch_scoreboard_data(start_date=start,
                                 end_date=date)[middle]


@pytest.fixture()
def get_engine():
    return start_engine(db_url)


def test_connection_for_local_dev_db(get_engine):
    assert_that(get_engine.connect()).is_type_of(Connection)
