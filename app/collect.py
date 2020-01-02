"""
Functions for collecting the endpoints data from NBA.com
using nba-api.
Auhtor: Maciej Cisowski
"""


import logging, logging.config
from config import LOGGING
from pandas import date_range
from datetime import date
from nba_api.stats.endpoints import scoreboardv2


logging.config.dictConfig(LOGGING)
logger = logging.getLogger("nba_v2.collect")


def fetch_scoreboard_data(start_date: date = None, end_date: date = None) -> dict:
    """
    Uses nba-api Scoreboard endpoint to retrieve a dict of all
    Scoreboard items as pandas Data Frames. Scoreboard items are:
    GameHeader, LineScore, SeriesStandings, LastMeeting,
    EastConfStandingsByDay, WestConfStandingsByDay, TeamLeaders,
    Available, TicketLinks, WinProbability

    The output dict is structured as:
    {
        date: {
            itemName: pandas DataFrame,
            itemName: pandas DataFrame
            ...
        }
    }

    :param start_date: datetime.date object representing start date
    :param end_date: datetime.date object representing end date
    :return: period_out dict of daily dicts with DataFrame objects
    :rtype: dict
    """
    period_out = {}
    logger.info("Looping through dates for scoreboard data")
    for d in date_range(start=start_date, end=end_date).to_pydatetime():
        day = d.strftime("%Y/%m/%d")
        logger.debug(f"Getting scoreboard data for date: {day}")
        endpoint = scoreboardv2.ScoreboardV2(game_date=day)
        headers = endpoint.get_available_data()
        frames = endpoint.get_data_frames()
        logger.debug(f"Packing output for {d} into dict")
        period_out[day] = {k: v for k, v in zip(headers, frames)}
    logger.info(f"Found {len(period_out)} items after looping through"
                f" scoreboard data.")
    return period_out
