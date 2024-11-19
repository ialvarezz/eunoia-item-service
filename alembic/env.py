import os
import asyncio
from sqlalchemy.engine import Connection
from app.database import DATABASE_URL, engine
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import pool, engine_from_config
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from app.models import Base


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
load_dotenv()
config = context.config

# Retrieve the DATABASE_URL from the environment and set it in Alembic config
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set in the environment.")
print(database_url)
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
else:
    print("config is none")

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = engine

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)



if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
