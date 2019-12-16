import logging

from app.db.session import db_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    try:
        # Attempt to create a DB session,
        # this will serve to check if DB is awake
        db_session.execute('SELECT 1')
    except Exception as e:
        logger.error(e)
        raise e


def main():
    logger.info("Service initialization started...")
    init()
    logger.info("...service initialization finished")


if __name__ == "__main__":
    main()
