"""
Configuration dicts for the NBA_v2 app
Author: Maciej Cisowski
"""
from enum import Enum


# app name
NBA_APP_NAME = "NBA"

# timeout defaults
TIMEOUT_INTERVAL = 30
TIMEOUT_SECS = 60

# logger config
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
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
            "maxBytes": 20480,
            "backupCount": 3,
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


class DbActions(Enum):
    FAIL = "fail"
    REPLACE = "replace"
    APPEND = "append"


# default values for the db config; overwrite with same-named env vars for secrets
DB = {
    "NBA_DB_URL": 'sqlite://',
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
        }
    }
}
