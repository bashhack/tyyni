import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.session import db_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_attempt_number = 60 * 5  # Five (5) minutes
wait_time = 1  # One (1) second


@retry(
    stop=stop_after_attempt(max_attempt_number=max_attempt_number),
    wait=wait_fixed(wait=wait_time),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init():
    try:
        # Attempt to create a DB session,
        # this will serve to check if DB is awake
        db_session.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def main():
    logger.info("Service initialization started...")
    init()
    logger.info("...service initialization finished")


if __name__ == "__main__":
    main()
