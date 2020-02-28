"""
Database connection setup for the NBA_v2 app.
Author: Maciej Cisowski
"""
from pandas import DataFrame
from config import DB, LOGGING, DbActions
from models.monitor import Monitor, metadata
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import logging.config


# create logger for this module and configure it
logging.config.dictConfig(LOGGING)
logger = logging.getLogger("nba_v2.commit")


def start_engine(url: str = DB["NBA_DB_URL"]) -> Engine:
    """
    Creates an SQLAlchemy engine using the given url.
    :param url: like sqlite:// or postgres://<yourURL>, defaults to
    the NBA_DB_URL value in config.py
    :return: SQLAlchemy Engine instance
    """
    logger.info(f"Establishing db engine for: {url}")
    return create_engine(url, echo=True)


def get_db_table_offset(db_engine: Engine, table: str) -> int:
    """
    Query the given table with an SQLAlchemy engine connection
    and return the record offset for that table.
    :param db_engine: SQLAlchemy engine used to connect to the db
    :param table: name of the queried tabled
    :return: offset (count of) rows of the table
    :rtype: int
    """
    logger.debug(f"Checking if the table {table} exists on the db.")
    if db_engine.has_table(table):
        # this will return something like [(6, )], hence it's awkward
        offset = db_engine.execute(
            f"SELECT COUNT(*) FROM {table};").fetchall()[0][0]
        logger.debug(f"Offset for table {table} is {offset}")
        return offset
    else:
        logger.exception(f"Did not find table: {table} in db.")
        return 0


def post_monitor_data(db: Engine, data: Monitor) -> bool:
    """
    Posts batch monitoring data to a monitor db.
    :param db: SQLAlchemy Engine for the connection
    :param data: Monitor instance for stats
    :return: success or failure
    ":rtype: bool
    """

    # create the necessary tables
    try:
        metadata.create_all(bind=db,
                            tables=[data.__table__],
                            checkfirst=True)
    except OperationalError or SQLAlchemyError:
        logger.error("Could not create db table for monitor stats.")
        return False
    # create session for issuing commands to the db
    Session = sessionmaker(bind=db, expire_on_commit=True)
    session = Session()
    success = False
    try:
        logger.info('Attempting to add and commit monitor stats...')
        session.add(data)
        session.commit()
        success = True
    except OperationalError or SQLAlchemyError:
        logger.error("Errored out while trying to commit monitor stats.")
        return False
    finally:
        session.close()
    return success


def post_data(db: Engine,
              data: DataFrame,
              table: str,
              if_exists=DbActions) -> dict:
    """
    Attempts to post data to a SQL database using an SQLAlchemy
    engine. Returns a dict pair of {table: DataFrame size} that
    was processed.
    :param db: SQLAlchemy engine to call
    :param data: single pandas DataFrame to be posted
    :param table: the table name to use
    :param if_exists one of the DB_ACTIONS enum values for modifying
    how an existing db table should be treated
    :return: a dict pair of {table: DataFrame size}
    :rtype: dict
    """
    logger.info(f"Posting data to table: {table}.")
    try:
        data.to_sql(name=table, con=db, schema=None, if_exists=if_exists.value,
                    index=True)
    except OperationalError or SQLAlchemyError:
        logger.warning(f"Error while posting data to table: {table}")
        return {table: 0}
    return {table: len(data.index)}


def batch_upload(data: dict, db: Engine, batch_def: list) -> list:
    """
    Takes the output of fetch_scoreboard_data() as it's input, along
    with a SQLAlchemy Engine instance and a definition of what items
    are to be uploaded to the db.
    It will get the current offset in the target db, extract the item
    to be uploaded, attempt to upload it to the db and then validate
    the process with another fetch of the db offset. The result is a
    dict of the "before" and "after" offsets, indexed by upload item,
    and a "success" boolean, if the difference between offsets is
    equal to the size of the uploaded item.

    :param batch_def: a dict picking the items from Scoreboard that
    need to be uploaded
    :param data: Scoreboard data from fetch_scoreboard_data(),
    indexed by date, dict
    :param db: SQLAlchemy instance of Engine
    :return: list of Monitor SQLAlchemy objects
    :rtype: list
    """

    # reverse mapping for ease of access
    named = {i["name"]: i for i in batch_def}
    # output
    batch_upload_results = []

    for date_item in data:
        # cast the date string into a date object for db compliance
        date_object = datetime.strptime(date_item, "%Y/%m/%d").date()

        logger.info(f"Batch processing: looping through date items in {date_item}.")
        for item in data[date_item]:
            logger.info(f"Looping through items...")
            if item in named and not data[date_item][item].empty:
                logger.debug(f"Getting item details...")
                pre_offset = get_db_table_offset(db, named[item]["table"])
                post_offset = 0
                success = False
                size = data[date_item][item].count()[0]
                action = named[item]["action"]
                validate = True if action is not DbActions.REPLACE else False
                try:
                    logger.debug(f"Attempting db upload for {item}.")
                    post_data(db=db,
                              data=data[date_item][item],
                              table=named[item]["table"],
                              if_exists=action)
                    logger.debug(f"Getting post offset for {item}.")
                    post_offset = get_db_table_offset(
                        db, named[item]["table"])
                    logger.debug("Establishing success.")
                    success = False if \
                        validate and not (post_offset - pre_offset == size) \
                        else True
                except OperationalError or SQLAlchemyError:
                    logger.error("Errored out while performing batch upload. "
                                 "See logs.")
                    success = False
                finally:
                    logger.info("Packing monitor data...")
                    monitor = Monitor(
                        date=date_object,
                        item=str(item),
                        pre_offset=int(pre_offset),
                        post_offset=int(post_offset),
                        size=int(size),
                        success=bool(success)
                    )
                    batch_upload_results.append(monitor)
            else:
                logger.debug(f"Item: {item} not found in {named}")
    return batch_upload_results
