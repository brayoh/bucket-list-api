""" This class contains an instance of the sql alchemy
    database connection pool and methods for saving and deleting
    data in the database
"""
import logging
from app import db

logger = logging.getLogger(__name__)


def save_record(record):
    """ This function saves data to the db if transaction is successful. """
    try:
        db.session.add(record)
        db.session.commit()
    except Exception as err:
        logger.error(err)

def delete_record(record):
    """ This function deletes data from db if transaction is successful. """
    try:
        db.session.delete(record)
        db.session.commit()
    except Exception as err:
        logger.error(err)
