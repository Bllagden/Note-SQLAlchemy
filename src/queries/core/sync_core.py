from sqlalchemy import Integer, and_, func, insert, select, text, update

from db.engine import engine
from db.models import Workload, metadata_imp, resumes_tab, workers_tab


class SyncCore:
    @staticmethod
    def get_version():
        with engine.connect() as conn:
            stmt = "SELECT VERSION()"
            res = conn.execute(text(stmt))
            print("sync_version=", res.all(), sep="")

    @staticmethod
    def delete_tables():
        engine.echo = False
        metadata_imp.drop_all(engine)
        engine.echo = True

    @staticmethod
    def create_tables():
        print()
        metadata_imp.create_all(engine)

    @staticmethod
    def insert_workers(workers: list[str]):
        """statement: общий термин для любого запроса;
        query: извлечение данныз из БД (обычно SELECT)."""
        with engine.connect() as conn:
            print()
            # stmt = """INSERT INTO workers (username) VALUES
            #             ('AAA'),
            #             ('BBB');"""
            # conn.execute(text(stmt))

            # stmt = insert(workers_tab).values(
            #     [
            #         {"username": "AAA"},
            #         {"username": "BBB"},
            #     ]
            # )

            values = [{"username": name} for name in workers]
            stmt = insert(workers_tab).values(values)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with engine.connect() as conn:
            print()
            query = select(workers_tab)  # SELECT * FROM workers
            res = conn.execute(query)
            workers = res.all()
            print(f"{workers=}")  # [(1, 'AAA'), (2, 'BBB')]

    @staticmethod
    def update_worker_1(worker_id: int = 1, new_username: str = "UPDATE_CORE_AAA"):
        """Без SQL-инъекций (bindparams)"""
        with engine.connect() as conn:
            print()
            stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            stmt = stmt.bindparams(username=new_username, id=worker_id)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def update_worker_2(worker_id: int = 2, new_username: str = "UPDATE_CORE_BBB"):
        with engine.connect() as conn:
            print()
            stmt = (
                update(workers_tab)
                .values(username=new_username)
                .filter_by(id=worker_id)  # .where(workers_tab.c.id == worker_id)
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def insert_resumes():
        with engine.connect() as conn:
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
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        """
        SELECT workload, AVG(compensation)::INT AS avg_compensation
        FROM resumes
        WHERE title LIKE '%Python%' AND compensation > 40000
        GROUP BY workload
        HAVING AVG(compensation) > 70000
        """
        with engine.connect() as conn:
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
            res = conn.execute(query)
            result = res.all()
            print(result)
            print(result[0].avg_compensation)

    @staticmethod
    def insert_additional_resumes():
        with engine.connect() as conn:
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
            conn.execute(insert_workers)
            conn.execute(insert_resumes)
            conn.commit()
