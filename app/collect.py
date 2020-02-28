"""
Functions for collecting the endpoint's data from NBA.com
using nba-api by Swar Patel (swar): https://github.com/swar/nba_api
Auhtor: Maciej Cisowski
"""
import logging.config
from config import LOGGING, TIMEOUT_INTERVAL, TIMEOUT_SECS, request_header
from pandas import date_range
from time import sleep
from datetime import date, timedelta
from nba_api.stats.endpoints import scoreboardv2


# create logger for this module and configure it
logging.config.dictConfig(LOGGING)
logger = logging.getLogger("nba_v2.collect")


def fetch_scoreboard_data(start_date: date = date.today() - timedelta(days=1),
                          end_date: date = date.today() - timedelta(days=1),
                          timeout_days: int = TIMEOUT_INTERVAL,
                          timeout_secs: int = TIMEOUT_SECS) -> dict:
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
    It breaks up the requests into batches of <timeout_days> and
    waits <timeout_secs> between the batches to avoid throttling
    on the server end. This defaults to config values.

    :param timeout_secs: int for number of seconds to wait between
    request intervals
    :param timeout_days: number of days in a request interval
    :param start_date: datetime.date object representing start date,
    defaults to yesterday
    :param end_date: datetime.date object representing end date,
    defaults to yesterday
    :return: period_out dict of daily dicts with DataFrame objects
    :rtype: dict
    """
    period_out = {}
    logger.info("Looping through dates for scoreboard data")
    d_range = date_range(start=start_date, end=end_date).to_pydatetime()
    for d in d_range:
        # sleep for <timeout_secs> upon hitting the <timeout_days> count
        if (d_range.tolist().index(d) + 1) % timeout_days == 0:
            logger.debug(f"Sleeping for: {timeout_secs} secs")
            sleep(timeout_secs)
            logger.debug("Resuming execution")

        day = d.strftime("%Y/%m/%d")
        logger.debug(f"Getting scoreboard data for date: {day}")
        endpoint = scoreboardv2.ScoreboardV2(game_date=day,
                                             headers=request_header,
                                             timeout=300)
        headers = endpoint.get_available_data()
        frames = endpoint.get_data_frames()
        logger.debug(f"Packing output for {d} into dict")
        period_out[day] = {k: v for k, v in zip(headers, frames)}
    logger.info(f"Found {len(period_out)} items after looping through"
                f" scoreboard data.")
    return period_out
