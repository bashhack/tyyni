from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.core.config import SQLALCHEMY_DATABASE_URI
from app.db.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# To better support 12-Factor app principles, rather than
# hardcode a DB uri here, we'll follow the Alembic docs' advice:
#
#   sqlalchemy.url - A URL to connect to the database via SQLAlchemy. 
#   This configuration value is only used if the env.py file calls upon them; 
#   in the “generic” template, the call to config.get_main_option("sqlalchemy.url") 
#   in the run_migrations_offline() function and the call to engine_from_
#   config(prefix="sqlalchemy.") in the run_migrations_online() function are 
#   where this key is referenced. If the SQLAlchemy URL should come from 
#   some other source, such as from environment variables or a global registry, 
#   or if the migration environment makes use of multiple database URLs,
#   the developer is encouraged to alter the env.py file to use whatever
#   methods are appropriate in order to acquire the database URL or URLs.
#
#   Source: https://alembic.sqlalchemy.org/en/latest/tutorial.html

# There's a decent example here:
# https://allan-simon.github.io/blog/posts/python-alembic-with-environment-variables/


def get_url():
    return SQLALCHEMY_DATABASE_URI


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    
    url = get_url()  # using this in favor of: config.get_main_option("sqlalchemy.url") from the *.ini
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
