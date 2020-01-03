"""
Common utility functions for NBA_v2.
Author: Maciej Cisowski
"""
import os
import logging, logging.config
from config import LOGGING, NBA_APP_NAME

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('nba.common')


def update_config_with_env_vars(app_name: str = "NBA") -> dict:
    """
    Gets environment variables starting with the app name given in
    the config.py file. Based on env getter from my Meteo project.
    It defaults to the values in config.py and overwrites or appends
    that dict if an environment variable matches the
    <app_name> param.
    :param app_name: str - name of app, defaults to NBA
    :return: a dictionary of var name : var value pairs updated with
    env vars meeting the "starts with <app_name> criteria
    :rtype: dict
    """
    from config import DB
    db_out = DB.copy()
    logger.debug("Getting environment variables")
    variables = os.environ
    logger.debug(f"Filtering for env vars starting with: \"{app_name}\"")
    filtered = [x for x in list(variables.keys()) if x.startswith(app_name)]

    logger.info("Setting config values with environment parameters")
    for key in filtered:
        # if env var name is the same as cfg var, overwrite it's value
        if key in list(DB.keys()):
            db_out[key] = variables[key]
        # if env var is not in cfg, add it with env value
        else:
            db_out[key] = variables[key]
    logger.info("Config values set")
    return db_out
