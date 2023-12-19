from sqlalchemy import Integer, and_, func, select
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from db import Base
from db.engine import async_engine, async_session_factory
from db.models import ResumesOrm, WorkersOrm, Workload


class AsyncOrm:
    @staticmethod
    async def delete_tables():
        async with async_engine.begin() as conn:
            async_engine.echo = False
            await conn.run_sync(Base.metadata.drop_all)
            async_engine.echo = True

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            print()
            await conn.run_sync(Base.metadata.create_all)
