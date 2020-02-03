"""
An app for retrieving NBA stats and posting them to dbs
Author: Maciej Cisowski
"""


import config
import logging.config
import pandas as pd
from datetime import date
from app.common import update_config_with_env_vars, get_argv
from app.collect import fetch_scoreboard_data
from app.data import merge_line_score
from app.commit import batch_upload, start_engine, post_data


logging.config.dictConfig(config.LOGGING)
logger = logging.getLogger(__name__)


def main():
    logger.info("Running app: NBA_v2")
    logger.debug("Updating env variables...")
    env_vars = update_config_with_env_vars()
    args = get_argv()
    start = False
    end = False
    if "NBA_STARTDATE" in args:
        start = date.fromisoformat(args["NBA_STARTDATE"])
    if "NBA_ENDDATE" in args:
        end = date.fromisoformat(args["NBA_ENDDATE"])
    logger.info("Getting data...")
    if start and end:
        logger.info("Using provided start and end dates.")
        data = merge_line_score(
            fetch_scoreboard_data(
                start_date=start,
                end_date=end
            )
        )
    else:
        logger.info("Defaulting to yesterday as start and end date.")
        data = merge_line_score(
            fetch_scoreboard_data()
        )
    logger.info("Retrieved data.")
    logger.info(f"Pushing data to db at: {env_vars['NBA_DB_URL']}")
    results = batch_upload(data=data,
                 db=start_engine(env_vars["NBA_DB_URL"]),
                 batch_def=config.BATCHES['default'])
    logger.info(f"Pushing monitor stats to db at: {env_vars['NBA_MONITOR_DB_URL']}")
    monitor_data_frame = pd.DataFrame.from_dict(results)
    post_data(
        db=start_engine(env_vars["NBA_MONITOR_DB_URL"]),
        data=monitor_data_frame,
        table=config.DB["NBA_DB_MAPPING"]["monitor"]["table"],
        if_exists=config.DB["NBA_DB_MAPPING"]["monitor"]["action"].value)
    logger.info("Finished run.")


if __name__ == "__main__":
    main()
