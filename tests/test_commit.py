"""
Tests for the commit functions of NBA_v2
Author: Maciej Cisowski
"""

import pytest
import allure
from assertpy import assert_that
from sqlalchemy.engine import Connection
from datetime import date
from app.data import merge_line_score
from app.commit import start_engine, get_db_table_offset, post_data, batch_upload
from app.common import update_config_with_env_vars
from app.collect import fetch_scoreboard_data
from config import DB, BATCHES


@pytest.fixture()
def get_data_frame():
    dfmt = "%Y/%m/%d"
    start = date(2019, 12, 1)
    end = date(2019, 12, 3)
    middle = date(2019, 12, 2).strftime(dfmt)
    return merge_line_score(
        fetch_scoreboard_data(start_date=start, end_date=end))[middle]\



@pytest.fixture()
def get_multi_data_frames():
    dfmt = "%Y/%m/%d"
    start = date(2019, 12, 1)
    end = date(2019, 12, 3)
    middle = date(2019, 12, 2).strftime(dfmt)
    return merge_line_score(
        fetch_scoreboard_data(start_date=start, end_date=end))


@pytest.fixture()
def get_db_envs():
    return update_config_with_env_vars()


@pytest.fixture()
def get_engine(get_db_envs, request):
    engine = start_engine(get_db_envs['NBA_DB_URL'])

    def drop_added_tables():
        for t in engine.table_names():
            engine.execute(f"DROP TABLE {t};")

    request.addfinalizer(drop_added_tables)
    return engine


@pytest.fixture()
def initial_upload_to_dbs(get_engine, get_data_frame):
    df_line_score = get_data_frame[DB["NBA_DB_MAPPING"]["line_score"]["name"]]
    df_series_standings = get_data_frame[DB["NBA_DB_MAPPING"][
        "series_standings"]["name"]]
    df_last_meeting = get_data_frame[DB["NBA_DB_MAPPING"][
        "last_meeting"]["name"]]
    df_west_conf_standings = get_data_frame[DB["NBA_DB_MAPPING"][
        "west_conference_standings_by_day"]["name"]]
    df_east_conf_standings = get_data_frame[DB["NBA_DB_MAPPING"][
        "east_conference_standings_by_day"]["name"]]
    tables = [
        DB["NBA_DB_MAPPING"]["line_score"]["table"],
        DB["NBA_DB_MAPPING"]["series_standings"]["table"],
        DB["NBA_DB_MAPPING"]["last_meeting"]["table"],
        DB["NBA_DB_MAPPING"]["west_conference_standings_by_day"]["table"],
        DB["NBA_DB_MAPPING"]["east_conference_standings_by_day"]["table"],
    ]
    actions = [
        DB["NBA_DB_MAPPING"]["line_score"]["action"],
        DB["NBA_DB_MAPPING"]["series_standings"]["action"],
        DB["NBA_DB_MAPPING"]["last_meeting"]["action"],
        DB["NBA_DB_MAPPING"]["west_conference_standings_by_day"]["action"],
        DB["NBA_DB_MAPPING"]["east_conference_standings_by_day"]["action"],
    ]
    data_list = [df_line_score, df_series_standings, df_last_meeting,
                 df_west_conf_standings, df_east_conf_standings]
    data_table_action_list = zip(tables, data_list, actions)
    for item in data_table_action_list:
        item[1].to_sql(name=item[0], schema=None, if_exists=item[2].value,
                       con=get_engine)


def test_connection_for_local_dev_db(get_engine):
    assert_that(get_engine.connect()).is_type_of(Connection)


def test_committing_to_a_new_db_creates_new_db_and_table(get_engine, get_data_frame):
    df = get_data_frame[DB["NBA_DB_MAPPING"]["line_score"]["name"]]
    df.to_sql(name=DB["NBA_DB_MAPPING"]["line_score"]["table"],
              schema=None,
              if_exists=DB["NBA_DB_MAPPING"]["line_score"]["action"].value,
              con=get_engine)
    assert_that(
        get_engine.execute(
            f"SELECT * FROM {DB['NBA_DB_MAPPING']['line_score']['table']}").fetchall()).is_not_empty()


def test_committing_creates_the_expected_tables(get_engine, get_data_frame):
    pre_commit_table_count = len(get_engine.table_names())
    line_score = get_data_frame[DB["NBA_DB_MAPPING"]["line_score"]["name"]]
    series_standing = get_data_frame[DB["NBA_DB_MAPPING"]["series_standings"]["name"]]
    line_score.to_sql(name=DB["NBA_DB_MAPPING"]["line_score"]["table"],
                      schema=None,
                      if_exists=DB["NBA_DB_MAPPING"]["line_score"]["action"].value,
                      con=get_engine)

    series_standing.to_sql(name=DB["NBA_DB_MAPPING"]["series_standings"]["table"],
                           schema=None,
                           if_exists=DB["NBA_DB_MAPPING"]["series_standings"]["action"].value,
                           con=get_engine)
    post_commit_table_count = len(get_engine.table_names())

    assert_that(
        post_commit_table_count - pre_commit_table_count).is_equal_to(2)


def test_get_db_table_offset_returns_expected_size(
        get_engine, get_data_frame):
    df = get_data_frame[DB["NBA_DB_MAPPING"]["line_score"]["name"]]
    df_size = df["GAME_ID_away"].size
    df.to_sql(name=DB["NBA_DB_MAPPING"]["line_score"]["table"],
              schema=None,
              if_exists=DB["NBA_DB_MAPPING"]["line_score"]["action"].value,
              con=get_engine)
    offset = get_db_table_offset(get_engine,
                                 DB["NBA_DB_MAPPING"]["line_score"]["table"])
    assert_that(offset).is_equal_to(df_size)


def test_post_data_with_one_table_append_action_increases_db_offset_by_df_size(
        get_data_frame, get_engine):
    df = get_data_frame[DB["NBA_DB_MAPPING"]["line_score"]["name"]]
    df_size = df["GAME_ID_away"].size
    df.to_sql(name=DB["NBA_DB_MAPPING"]["line_score"]["table"],
              schema=None,
              if_exists=DB["NBA_DB_MAPPING"]["line_score"]["action"].value,
              con=get_engine)
    init_offset = get_db_table_offset(
        get_engine,
        DB["NBA_DB_MAPPING"]["line_score"]["table"])
    df.to_sql(name=DB["NBA_DB_MAPPING"]["line_score"]["table"],
              schema=None,
              if_exists=DB["NBA_DB_MAPPING"]["line_score"]["action"].value,
              con=get_engine)
    post_offset = get_db_table_offset(
        get_engine,
        DB["NBA_DB_MAPPING"]["line_score"]["table"])

    assert_that(post_offset - init_offset).is_equal_to(df_size)


def test_post_data_with_one_table_replace_action_returns_zero_offset(
        get_data_frame, get_engine):
    df = get_data_frame[DB["NBA_DB_MAPPING"]["east_conference_standings_by_day"]["name"]]
    df_size = df["TEAM_ID"].size
    df.to_sql(name=DB["NBA_DB_MAPPING"]["east_conference_standings_by_day"]["table"],
              schema=None,
              if_exists=DB["NBA_DB_MAPPING"]["east_conference_standings_by_day"]["action"].value,
              con=get_engine)
    init_offset = get_db_table_offset(
        get_engine,
        DB["NBA_DB_MAPPING"]["east_conference_standings_by_day"]["table"])
    df.to_sql(name=DB["NBA_DB_MAPPING"]["east_conference_standings_by_day"]["table"],
              schema=None,
              if_exists=DB["NBA_DB_MAPPING"]["east_conference_standings_by_day"]["action"].value,
              con=get_engine)
    post_offset = get_db_table_offset(
        get_engine,
        DB["NBA_DB_MAPPING"]["east_conference_standings_by_day"]["table"])

    assert_that(post_offset - init_offset).is_equal_to(0)


def test_batch_upload_for_one_day(get_data_frame,
                                  get_engine,
                                  initial_upload_to_dbs):
    result = batch_upload(data=get_data_frame, db=get_engine,
                          batch_def=BATCHES["default"])
    failures = [r["success"] for r in [result[i] for i in result]
                if r["success"] is False]
    assert_that(failures).is_empty()


def test_batch_upload_for_many_days(get_multi_data_frames,
                                    get_engine,
                                    initial_upload_to_dbs):
    result = batch_upload(data=get_multi_data_frames,
                          db=get_engine,
                          batch_def=BATCHES["default"])
    failures = [r["success"] for r in [result[i] for i in result]
                if r["success"] is False]
    assert_that(failures).is_empty()
