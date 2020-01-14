"""
Database connection setup for the NBA_v2 app.
Author: Maciej Cisowski
"""
from config import DB, LOGGING
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import logging.config


# create logger for this module and configure it
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('nba.commit')


def start_engine(url: str = DB["NBA_DB_URL"]) -> Engine:
    """
    Creates an SQLAlchemy engine using the given url.
    :param url: like sqlite:// or postgres://<yourURL>
    :return: SQLAlchemy Engine instance
    """
    logger.info(f"Establishing db engine for: {url}")
    return create_engine(url, echo=True)

URL = "postgres://ltjeysrdpkmdxq:5bd500e4e1ffb23ff9d49afa1cbe574320a8e5a6eee77f16d16ac5db114690da@ec2-174-129-18-98.compute-1.amazonaws.com:5432/ddbv6debpheef4"

from sqlalchemy.orm import sessionmaker
from models.scoreboard import LineScore
eng = start_engine(URL)
Session = sessionmaker(bind=eng)
session = Session()
q = session.query(LineScore)
for instance in session.query(LineScore).order_by(LineScore.id):
    print(instance.away_pts)


