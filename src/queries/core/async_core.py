from sqlalchemy import Integer, and_, func, insert, select, text, update
from sqlalchemy.exc import DBAPIError

from db import Base
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
        """ORM-запросы создают зависимости в БД, поэтому приходится удалять их через Base"""
        print()
        # async_engine.echo = False
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(metadata_imp.drop_all)

        except DBAPIError as e:
            async with async_engine.begin() as conn:
                if "DependentObjectsStillExistError" in str(e):  #  exc from asyncpg
                    await conn.run_sync(Base.metadata.drop_all)
                else:
                    raise e
        # async_engine.echo = True

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            print()
            await conn.run_sync(metadata_imp.create_all)

    @staticmethod
    async def insert_workers(workers: list[str]):
        """statement: общий термин для любого запроса;
        query: извлечение данныз из БД (обычно SELECT)."""
        async with async_engine.connect() as conn:
            print()
            values = [{"username": name} for name in workers]
            stmt = insert(workers_tab).values(values)
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def select_workers():
        async with async_engine.connect() as conn:
            print()
            query = select(workers_tab)  # SELECT * FROM workers
            res = await conn.execute(query)
            workers = res.all()
            print(f"{workers=}")  # [(1, 'AAA'), (2, 'BBB')]

    @staticmethod
    async def update_worker_1(worker_id: int = 1, new_username: str = "UPDATE_CR_AAA"):
        """Без SQL-инъекций (bindparams)"""
        async with async_engine.connect() as conn:
            print()
            stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            stmt = stmt.bindparams(username=new_username, id=worker_id)
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def update_worker_2(worker_id: int = 2, new_username: str = "UPDATE_CR_BBB"):
        async with async_engine.connect() as conn:
            print()
            stmt = (
                update(workers_tab)
                .values(username=new_username)
                .filter_by(id=worker_id)  # .where(workers_tab.c.id == worker_id)
            )
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def insert_resumes():
        async with async_engine.connect() as conn:
            print()
            resumes = [
                {
                    "title": "Python Junior Developer",
                    "compensation": 50000,
                    "workload": Workload.fulltime,
                    "worker_id": 1,
                },
                {
                    "title": "Python Разработчик",
                    "compensation": 150000,
                    "workload": Workload.fulltime,
                    "worker_id": 1,
                },
                {
                    "title": "Python Data Engineer",
                    "compensation": 250000,
                    "workload": Workload.parttime,
                    "worker_id": 2,
                },
                {
                    "title": "Data Scientist",
                    "compensation": 300000,
                    "workload": Workload.fulltime,
                    "worker_id": 2,
                },
            ]
            stmt = insert(resumes_tab).values(resumes)
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def select_resumes_avg_compensation(like_language: str = "Python"):
        """
        SELECT workload, AVG(compensation)::INT AS avg_compensation
        FROM resumes
        WHERE title LIKE '%Python%' AND compensation > 40000
        GROUP BY workload
        HAVING AVG(compensation) > 70000
        """
        async with async_engine.connect() as conn:
            print()
            query = (
                select(
                    resumes_tab.c.workload,
                    func.avg(resumes_tab.c.compensation)
                    .cast(Integer)
                    .label("avg_compensation"),
                )
                .select_from(resumes_tab)
                .filter(
                    and_(
                        resumes_tab.c.title.contains(like_language),
                        resumes_tab.c.compensation > 40000,
                    )
                )
                .group_by(resumes_tab.c.workload)
                .having(func.avg(resumes_tab.c.compensation) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await conn.execute(query)
            result = res.all()
            print(result)
            print(result[0].avg_compensation)

    @staticmethod
    async def insert_additional_resumes():
        async with async_engine.connect() as conn:
            print()
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},  # id 5
            ]
            resumes = [
                {
                    "title": "Python программист",
                    "compensation": 60000,
                    "workload": "fulltime",
                    "worker_id": 3,
                },
                {
                    "title": "Machine Learning Engineer",
                    "compensation": 70000,
                    "workload": "parttime",
                    "worker_id": 3,
                },
                {
                    "title": "Python Data Scientist",
                    "compensation": 80000,
                    "workload": "parttime",
                    "worker_id": 4,
                },
                {
                    "title": "Python Analyst",
                    "compensation": 90000,
                    "workload": "fulltime",
                    "worker_id": 4,
                },
                {
                    "title": "Python Junior Developer",
                    "compensation": 100000,
                    "workload": "fulltime",
                    "worker_id": 5,
                },
            ]
            insert_workers = insert(workers_tab).values(workers)
            insert_resumes = insert(resumes_tab).values(resumes)
            await conn.execute(insert_workers)
            await conn.execute(insert_resumes)
            await conn.commit()

    # Relationships отсутствуют при использовании Table
