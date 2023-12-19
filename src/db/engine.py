"""
engine - высокоуровневый API SQLAlchemy для работы с БД через драйвер.
session - работа с БД в стиле транзакций.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import db_settings

engine = create_engine(
    url=db_settings.url_psycopg,
    echo=True,
)

async_engine = create_async_engine(
    url=db_settings.url_asyncpg,
    echo=True,
)

session_factory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
