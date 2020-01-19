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


def get_db_table_offset(db_engine: Engine, table: str) -> int:
    """
    Query the given table with an SQLAlechemy engine connection
    and return the record offset for that table.
    :param db_engine: SQLAlchemy engine used to connect to the db
    :param table: name of the queried tabled
    :return: offest (count of) rows of the table
    :rtype: int
    """
    logger.debug(f"Checking if the table {table} exists on the db.")
    if db_engine.has_table(table):
        # this will return something like [(6, )], therefore the awkward accessors
        offset = db_engine.execute(
            f"SELECT COUNT(*) FROM {table};").fetchall()[0][0]
        logger.debug(f"Offset for table {table} is {offset}")
        return offset
    else:
        logger.exception(f"Did not find table: {table} in db.")
        raise LookupError(f"Did not find table: {table} in db.")

# from sqlalchemy.orm import sessionmaker
# from models.scoreboard import LineScore
# eng = start_engine(URL)
# Session = sessionmaker(bind=eng)
# session = Session()
# q = session.query(LineScore)
# for instance in session.query(LineScore).order_by(LineScore.id):
#     print(instance.away_pts)


