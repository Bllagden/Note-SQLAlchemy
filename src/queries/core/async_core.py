from sqlalchemy import Integer, and_, func, insert, select, text, update

from db.engine import async_engine
from db.models import Workload, metadata_imp, resumes_tab, workers_tab


class AsyncCore:
    @staticmethod
    async def get_version():
        async with async_engine.connect() as conn:
            stmt = "SELECT VERSION()"
            res = await conn.execute(text(stmt))
            print("async_version=", res.all(), sep="")

    @staticmethod
    async def delete_tables():
        async with async_engine.begin() as conn:
            async_engine.echo = False
            await conn.run_sync(metadata_imp.drop_all)
            async_engine.echo = True

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            print()
            await conn.run_sync(metadata_imp.create_all)
