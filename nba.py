"""
An app for retrieving NBA stats and posting them to dbs
Author: Maciej Cisowski
"""


import config
import pandas
import logging, logging.config


logging.config.dictConfig(config.LOGGING)
logger = logging.getLogger(__name__)


def main():
    logger.info("Running app: NBA_v2")


if __name__ == "__main__":
    main()