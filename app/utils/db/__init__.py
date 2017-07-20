import logging
from app import db

logger = logging.getLogger(__name__)

def save_data(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        logger.error(e)
        raise e
