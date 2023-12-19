from sqlalchemy import Integer, and_, func, select
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from db import Base
from db.engine import engine, session_factory
from db.models import ResumesOrm, WorkersOrm, Workload


class SyncOrm:
    @staticmethod
    def delete_tables():
        engine.echo = False
        Base.metadata.drop_all(engine)
        engine.echo = True

    @staticmethod
    def create_tables():
        print()
        Base.metadata.create_all(engine)

    @staticmethod
    def insert_workers(workers: list[str]):
        with session_factory() as session:
            print()
            for name in workers:
                new_worker = WorkersOrm(username=name)
                session.add(new_worker)
                # session.add_all([new_worker, ...])
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            print()
            # worker_id = 1
            # worker = session.get(WorkersOrm, worker_id)

            query = select(WorkersOrm)  # SELECT * FROM workers
            res = session.execute(query)
            # workers = res.all()  # list[tuple[IterOrm]]
            workers = res.scalars().all()  # list[IterOrm]
            print(f"{workers=}")
