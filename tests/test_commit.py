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
from app.commit import start_engine, get_db_table_offset
from app.common import update_config_with_env_vars
from app.collect import fetch_scoreboard_data


class TestDB(object):
    lookup = {
        "SQLiteTableNumQuery": "SELECT name FROM sqlite_master "
                               "WHERE type='table' "
                               "AND name NOT LIKE 'sqlite_%';",
        "LineScore": {
            "df": "mergedLineScore",
            "table": "line_score",
            "query": "SELECT * FROM line_score;"
        },
        "SeriesStandings": {
            "df": "SeriesStandings",
            "table": "series_standings",
            "query": "SELECT * FROM series_standings;"
        },
        "WestConfStandingsByDay": {
            "df": "WestConfStandingsByDay",
            "table": "west_conf_standings_by_day",
            "query": "SELECT * FROM west_conf_standings_by_day;"
        },
        "EastConfStandingsByDay": {
            "df": "EastConfStandingsByDay",
            "table": "east_conf_standings_by_day",
            "query": "SELECT * FROM west_conf_standings_by_day;"
        }
    }

    @pytest.fixture()
    def get_data_frame(self):
        dfmt = "%Y/%m/%d"
        start = date(2019, 12, 1)
        end = date(2019, 12, 3)
        middle = date(2019, 12, 2).strftime(dfmt)
        return merge_line_score(
            fetch_scoreboard_data(start_date=start, end_date=end))[middle]

    @pytest.fixture()
    def get_db_envs(self):
        return update_config_with_env_vars()

    @pytest.fixture()
    def get_engine(self, get_db_envs, request):
        engine = start_engine(get_db_envs['NBA_DB_URL'])

        def drop_added_tables():
            for t in engine.execute(
                    self.lookup["SQLiteTableNumQuery"]).fetchall():
                engine.execute(f"DROP TABLE {t[0]};")

        request.addfinalizer(drop_added_tables)
        return engine

    def test_connection_for_local_dev_db(self, get_engine):
        assert_that(get_engine.connect()).is_type_of(Connection)

    def test_committing_to_a_new_db_creates_new_db_and_table(self, get_engine, get_data_frame):
        db = get_engine
        df = get_data_frame[self.lookup["LineScore"]["df"]]
        df.to_sql(name=self.lookup["LineScore"]["table"],
                  schema=None,
                  if_exists='replace',
                  con=db)
        assert_that(
            db.execute(
                self.lookup["LineScore"]["query"]
            ).fetchall()).is_not_empty()

    def test_committing_creates_the_expected_tables(self, get_engine, get_data_frame):
        db = get_engine
        pre_commit_table_count = len(db.execute(
            self.lookup["SQLiteTableNumQuery"]
        ).fetchall())

        line_score = get_data_frame[self.lookup["LineScore"]["df"]]
        series_standing = get_data_frame[self.lookup["SeriesStandings"]["df"]]

        line_score.to_sql(name=self.lookup["LineScore"]["table"],
                          schema=None,
                          if_exists='replace',
                          con=db)

        series_standing.to_sql(name=self.lookup["SeriesStandings"]["table"],
                               schema=None,
                               if_exists='replace',
                               con=db)

        post_commit_table_count = len(db.execute(
            self.lookup["SQLiteTableNumQuery"]).fetchall()
        )

        assert_that(
            post_commit_table_count - pre_commit_table_count).is_equal_to(2)

    def test_get_db_table_offset_returns_expected_size(self,
                                             get_engine,
                                             get_data_frame):
        db = get_engine
        df = get_data_frame[self.lookup["LineScore"]["df"]]
        df_size = df["GAME_ID_away"].size
        df.to_sql(name=self.lookup["LineScore"]["table"],
                  schema=None,
                  if_exists='replace',
                  con=db)
        offset = get_db_table_offset(db, self.lookup["LineScore"]["table"])
        assert_that(offset).is_equal_to(df_size)

