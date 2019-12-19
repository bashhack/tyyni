import logging

from app.db.init_db import init_db
from app.db.session import db_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    init_db(db_session)


def main():
    logger.info("Seeding initial data...")
    init()
    logger.info("...seed data created")


if __name__ == "__main__":
    main()
