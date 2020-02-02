"""
Database connection setup for the NBA_v2 app.
Author: Maciej Cisowski
"""
from pandas import DataFrame
from config import DB, LOGGING, DbActions
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import logging.config


# create logger for this module and configure it
logging.config.dictConfig(LOGGING)
logger = logging.getLogger("nba_v2.commit")


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


def post_data(db: Engine, data: DataFrame, table: str, if_exists=DbActions) -> dict:
    """
    Attempts to post data to a SQL database using an SQLAlchemy
    engine. Returns a dict pair of {table: DataFrame size} that
    was processed.
    :param db: SQLAlechemy engine to call
    :param data: single pandas DataFrame to be posted
    :param table: the table name to use
    :param if_exists one of the DB_ACTIONS enum values for modifying
    how an existing db table should be treated
    :return: a dict pair of {table: DataFrame size}
    :rtype: dict
    """
    logger.info(f"Posting data to table: {table}.")
    try:
        data.to_sql(name=table, con=db, schema=None, if_exists=if_exists,
                    index=True)
    except OperationalError or SQLAlchemyError:
        logger.warning(f"Error while posting data to table: {table}")
        return {table: 0}
    return {table: len(data.index)}


def batch_upload(data: DataFrame, db: Engine, batch_def: list) -> dict:
    """
    Takes the output of fetch_scoreboard_data() as it's input, along
    with a SQLAlchemy Engine instance and a definition of what items
    are to be uploaded to the db.
    It will get the current offset in the target db, extract the item
    to be uploaded, attempt to upload it to the db and then validate
    the process with another get of the db offset. The result is a
    dict of the "before" and "after" offsets, indexed by upload item,
    and a "success" boolean, if the difference between offsets is
    equal to the size of the uploaded item.

    :param batch_def: a dict picking the items from Scoreboard that
    need to be uploaded
    :param data: Scoreboard data from fetch_scoreboard_data(),
    indexed by date
    :param db: SQLAlchemy instance of Engine
    :return: mapping of {"item": "init_offset", "after_offset",
    "success"}
    :rtype: dict
    """

    # reverse mapping for ease of access
    named = {i["name"]: i for i in batch_def}
    # output
    batch_upload_results = {}

    for date_item in data:
        logger.info("Batch processing: looping through date items in data.")
        for item in date_item:
            logger.info("Looping through items in date")
            if item in named:
                logger.debug(f"Getting item details for {item}.")
                pre_offset = get_db_table_offset(db, named[item]["table"])
                post_offset = 0
                size = data[item].count()[0]
                action = named[item]["action"]
                validate = True if action is not DbActions.REPLACE else False
                try:
                    logger.debug(f"Attempting db upload for {item}.")
                    post_data(db=db,
                              data=data[item],
                              table=named[item]["table"],
                              if_exists=action.value)
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
                    output = {
                        "pre_offset": pre_offset,
                        "post_offset": post_offset,
                        "size": size,
                        "success": success
                    }
                    # pack up the output to output dict
                    batch_upload_results[item] = output
    return batch_upload_results


# from sqlalchemy.orm import sessionmaker
# from app.common import update_config_with_env_vars
# import pandas as pd
# eng = start_engine(update_config_with_env_vars()["NBA_DB_URL"])
# Session = sessionmaker(bind=eng)
# session = Session()
# df1 = pd.DataFrame.from_dict({"1": ["woah", "noah"]})
# df2 = pd.DataFrame.from_dict({})
# df1.to_sql("empty_upload", eng, if_exists="replace")
# size1 = session.execute("SELECT COUNT(*) FROM empty_upload").fetchall()
# df2.to_sql("empty_upload", eng, if_exists="append")
# df2.to_sql("empty_upload", eng, if_exists="append")
# df2.to_sql("empty_upload", eng, if_exists="append")
# df2.to_sql("empty_upload", eng, if_exists="append")
# size2 = session.execute("SELECT COUNT(*) FROM empty_upload").fetchall()
# print(size1, size2)
# session.commit()
# session.close()

