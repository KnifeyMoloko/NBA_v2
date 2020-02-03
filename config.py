"""
Configuration dicts for the NBA_v2 app
Author: Maciej Cisowski
"""
from enum import Enum


# app name
NBA_APP_NAME = "NBA"

# timeout defaults
TIMEOUT_INTERVAL = 15
TIMEOUT_SECS = 180

# logger config
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": '%(asctime)s::%(name)s::%(levelname)s::%(message)s',
            "datefmt": '%Y-%m-%d %I:%M:%S'
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "simple",
            "maxBytes": 10480,
            "backupCount": 5,
            "filename": "./tests/logs/nba_test.log"
        }
    },
    "loggers": {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}

# custom request headers
request_header = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    #'Upgrade-Insecure-Requests': '1',
    "Referer": "https://stats.nba.com",
    "Origin": "https://stats.nba.com",
    "x-nba-stats-token": "true",
    "x-nba-stats-origin": "stats",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}


class DbActions(Enum):
    FAIL = "fail"
    REPLACE = "replace"
    APPEND = "append"


# default values for the db config; overwrite with same-named env vars for secrets
DB = {
    "NBA_DB_URL": 'sqlite://',
    "NBA_MONITOR_DB_URL": "sqlite://",
    "NBA_DB_MAPPING": {
        "line_score": {
            "name": "mergedLineScore",
            "table": "line_score",
            "action": DbActions.APPEND,
        },
        "series_standings": {
            "name": "SeriesStandings",
            "table": "series_standings",
            "action": DbActions.APPEND
        },
        "west_conference_standings_by_day": {
            "name": "WestConfStandingsByDay",
            "table": "west_conference_standings_by_day",
            "action": DbActions.REPLACE
        },
        "east_conference_standings_by_day": {
            "name": "EastConfStandingsByDay",
            "table": "east_conference_standings_by_day",
            "action": DbActions.REPLACE
        },
        "last_meeting": {
            "name": "LastMeeting",
            "table": "last_meeting",
            "action": DbActions.APPEND
        },
        "monitor": {
            "name": "monitor",
            "table": "monitor",
            "action": DbActions.APPEND
        }
    }
}

BATCHES = {
    "default": [DB["NBA_DB_MAPPING"]["line_score"],
                DB["NBA_DB_MAPPING"]["series_standings"],
                DB["NBA_DB_MAPPING"]["last_meeting"],
                DB["NBA_DB_MAPPING"]["west_conference_standings_by_day"],
                DB["NBA_DB_MAPPING"]["east_conference_standings_by_day"]]
}
