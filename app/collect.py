"""
Functions for collecting the endpoints data from NBA.com
using nba-api.
Auhtor: Maciej Cisowski
"""


from datetime import date
from nba_api.stats.endpoints import scoreboardv2


def fetch_scoreboard_data(start_date: date = None, end_date: date = None) -> dict:
    return {}
