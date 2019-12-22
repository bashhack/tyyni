from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import SQLALCHEMY_DATABASE_URI

# Create a database connection
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

# Create a registry of Session objects using a session factory instance via sessionmaker
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Create a session factory instance (for use in executing model queries, etc.)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# NOTE:
#       `This pattern allows disparate sections of the application to call
#       upon a global scoped_session, so that all those areas may share the
#       same session without the need to pass it explicitly.`
#
# For more on this pattern and the usages here, see:
# https://docs.sqlalchemy.org/en/13/orm/contextual.html
