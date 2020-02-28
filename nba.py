"""
An app for retrieving NBA stats using nba-api by
Swar Patel (swar): https://github.com/swar/nba_api, processing them
and committing to a db via SQLAlchemy ORM.
Author: Maciej Cisowski
"""
import config
import logging.config
from datetime import date
from app.common import update_config_with_env_vars, get_argv
from app.collect import fetch_scoreboard_data
from app.data import merge_line_score
from app.commit import batch_upload, start_engine, post_monitor_data


# set up logger using config
logging.config.dictConfig(config.LOGGING)
logger = logging.getLogger(__name__)


def main():
    logger.info(f"Running app: {config.NBA_APP_NAME}")
    logger.debug("Updating env variables...")
    env_vars = update_config_with_env_vars()
    logger.debug("Getting runtime parameters...")
    args = get_argv()
    start = False
    end = False
    if "NBA_STARTDATE" in args:
        start = date.fromisoformat(args["NBA_STARTDATE"])
    if "NBA_ENDDATE" in args:
        end = date.fromisoformat(args["NBA_ENDDATE"])
    logger.info("Getting data...")
    if start and end:
        logger.info(f"Using provided start: {start} "
                    f"and end {end} dates.")
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
    for result in results:
        post_monitor_data(db=start_engine(env_vars['NBA_MONITOR_DB_URL']),
                          data=result)
    logger.info("Finished pushing monitor stats.")
    logger.info("Finished run!")


if __name__ == "__main__":
    main()
