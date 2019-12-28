"""
Logger configuration dict for the NBA_v2 app
Author: Maciej Cisowski
"""

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
            "maxBytes": 2048,
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