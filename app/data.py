"""
Data manipulation functions for the NBA_v2 app.
Author: Maciej Cisowski
"""
import pandas as pd
import logging.config
from config import LOGGING
from datetime import date

# create logger for this module and configure it
logging.config.dictConfig(LOGGING)
logger = logging.getLogger("nba_v2.data")


def is_empty(scoreboard_data: dict,
             d: str = date.today().strftime("%Y/%m/%d")) -> bool:
    """
    Check if the "Available" dict item in scoreboard_data is an empty
    Data Frame
    :param scoreboard_data:
    :param d: date that should be checked, default to today
    :return: true if Available is empty, false otherwise
    :rtype: bool
    """
    logger.info(f"Checking if there are games on: {d}")
    return scoreboard_data[d]["Available"].empty


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

    for d in date_keys:
        if is_empty(scoreboard_data, d):
            logger.debug(f"Skipping merging for date: {d}")
            scoreboard_data[d]["mergedLineScore"] = pd.DataFrame.from_dict({})
        else:
            logging.debug(f"Performing merging for date: {d}")
            line_score = scoreboard_data[d].get("LineScore")
            away = line_score[line_score.index % 2 == 0]
            home = line_score[line_score.index % 2 != 0]
            scoreboard_data[d]["mergedLineScore"] = pd.merge(
                left=away,
                right=home,
                on="GAME_SEQUENCE",
                suffixes=("_away", "_home")
            )
    return scoreboard_data


# from pprint import pprint
# from app.collect import fetch_scoreboard_data
# from datetime import date
# x = merge_line_score(fetch_scoreboard_data(start_date=date(2019, 11, 27), end_date=date(2019, 11, 29)))
# for item in x:
#     pprint(x[item])

