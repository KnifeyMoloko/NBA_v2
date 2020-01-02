"""
Database connection setup for the NBA_v2 app.
Author: Maciej Cisowski
"""
from config import DB, LOGGING
from sqlalchemy import create_engine
import logging, logging.config


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('nba.commit')


def start_engine(url=DB["url"]):
    logger.info(f"Establishing db engine for {url}")
    return create_engine(url)

