"""
Tests for the common functions for NBA_v2
Author: Maciej Cisowski
"""

import pytest
import allure
import re
from assertpy import assert_that
from app.common import update_config_with_env_vars, get_argv


class TestCommon(object):
    params = {
        "app_name": "NBA",
        "nba_db_url": "sqlite",
        "nba_db_username": "nba",
        "nba_db_pswrd": "NBATestPassword",
        "wrong_entry": "https://localhost:-80808088080"
    }

    @pytest.fixture()
    def set_up_env_vars(self, monkeypatch):
        monkeypatch.setenv("NBA_USERNAME", self.params['nba_db_username'])
        monkeypatch.setenv("NBA_DB_URL", self.params['nba_db_url'])
        monkeypatch.setenv("NBA_DB_PSWRD", self.params['nba_db_pswrd'])

    @pytest.fixture()
    def set_up_env_vars_wrong(self, monkeypatch):
        monkeypatch.setenv("NBA_USERNAME", self.params['nba_db_username'])
        monkeypatch.setenv("NBA_DB_URL", self.params['nba_db_url'])
        monkeypatch.setenv("NBA_DB_PSWRD", self.params['nba_db_pswrd'])
        monkeypatch.setenv("wrong", self.params.get("wrong_entry"))

    def test_get_env_args_returns_dict(set_up_env_vars):
        assert_that(update_config_with_env_vars()).is_type_of(dict)

    def test_get_env_args_returns_non_empty_dict(set_up_env_vars):
        assert_that([update_config_with_env_vars().items()]).is_not_empty()

    def test_get_env_args_returns_dict_with_keywords_starting_with_app_name(self, set_up_env_vars):
        names = list(update_config_with_env_vars().keys())
        non_compliant = [i for i in names if not i.startswith(self.params.get("app_name"))]
        assert_that(non_compliant).is_empty()

    def test_get_env_args_does_not_contain_wrong_entry(self, set_up_env_vars_wrong):
        names = list(update_config_with_env_vars().keys())
        assert_that(self.params.get("wrong_entry")).is_not_in(names)

    def test_get_env_overwrites_default_values(self, set_up_env_vars):
        assert_that(update_config_with_env_vars()["NBA_DB_URL"]).matches(self.params.get("nba_db_url"))

    def test_get_argv_returns_dict(self, sdate, edate):
        assert_that(get_argv()).is_type_of(dict)

    def test_get_argv_returns_dict_with_filtered_items_only(self, sdate, edate):
        from config import NBA_APP_NAME
        item_names = list(get_argv().keys())
        non_compliant = [i for i in item_names if not i.startswith(NBA_APP_NAME)]
        assert_that(non_compliant).is_empty()

    @pytest.mark.parametrize("date_name", ["NBASTARTDATE", "NBAENDDATE"])
    def test_get_argv_has_date_items(self, date_name, sdate, edate):
        assert_that(list(get_argv().keys())).contains(date_name)
