"""
An app for retrieving NBA stats and posting them to dbs
Author: Maciej Cisowski
"""


import config
import pandas
import logging, logging.config
from nba_api.stats.endpoints import scoreboardv2 as sboard


logging.config.dictConfig(config.LOGGING)
logger = logging.getLogger(__name__)


def main():
    from pprint import pprint
    logger.info("Running app: NBA_v2")
    board = sboard.ScoreboardV2()
    data = board.get_available_data()
    dframes = board.get_data_frames()
    print(data)
    print()
    pprint(dframes)


if __name__ == "__main__":
    main()