"""
Database connection setup for the NBA_v2 app.
Author: Maciej Cisowski
"""
from config import DB, LOGGING
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import logging, logging.config


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('nba.commit')


def start_engine(url=DB["url"]) -> Engine:
    logger.info(f"Establishing db engine for {url}")
    return create_engine(url)
