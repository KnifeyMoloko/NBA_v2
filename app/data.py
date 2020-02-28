"""
Data manipulation functions for the NBA_v2 app.
Author: Maciej Cisowski
"""
import pandas as pd
import logging.config
from config import LOGGING
from datetime import date, timedelta

# create logger for this module and configure it
logging.config.dictConfig(LOGGING)
logger = logging.getLogger("nba_v2.data")


def is_empty(scoreboard_data: dict,
             check_date: str = (date.today() - timedelta(days=1))
             .strftime("%Y/%m/%d")) -> bool:
    """
    Check if the "Available" dict item in scoreboard_data is an empty
    Data Frame
    :param scoreboard_data:
    :param check_date: date that should be checked, default to yesterday
    :return: true if Available is empty, false otherwise
    :rtype: bool
    """
    logger.info(f"Checking if there are games on: {check_date}")
    return scoreboard_data[check_date]["Available"].empty


def merge_line_score(scoreboard_data: dict) -> dict:
    """
    Loop through the output of the collect function
    fetch_scoreboard_data() and return a DataFrame merged on the game
    sequence value.
    :param scoreboard_data: dict with items containing <line_score>
    members
    :return: scoreboard_data dict with <merged_line_score> output
    :rtype: dict
    """
    date_keys = list(scoreboard_data.keys())

    for date_key in date_keys:
        if is_empty(scoreboard_data, date_key):
            logger.debug(f"Skipping merging for date: {date_key}")
            scoreboard_data[date_key]["mergedLineScore"] = pd.DataFrame.\
                from_dict({})
        else:
            logging.debug(f"Performing merging for date: {date_key}")
            line_score = scoreboard_data[date_key].get("LineScore")
            away = line_score[line_score.index % 2 == 0]
            home = line_score[line_score.index % 2 != 0]
            # merge the home and away records on GAME_SEQUENCE,
            # set the suffixes
            scoreboard_data[date_key]["mergedLineScore"] = pd.merge(
                left=away,
                right=home,
                on="GAME_SEQUENCE",
                suffixes=("_away", "_home")
            )
    return scoreboard_data
