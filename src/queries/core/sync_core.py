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
