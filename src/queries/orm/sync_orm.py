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

    @staticmethod
    def update_worker_1(worker_id: int = 1, new_username: str = "UPDATE_ORM_AAA"):
        """Через session.get - два запроса (получаем и обновляем объект).
        Через CORE один запрос (UPDATE)"""
        with session_factory() as session:
            print()
            worker = session.get(WorkersOrm, worker_id)
            worker.username = new_username  # type: ignore
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            print()
            worker_1_resume_1 = ResumesOrm(
                title="Python Junior Developer",
                compensation=50000,
                workload=Workload.fulltime,
                worker_id=1,
            )
            worker_1_resume_2 = ResumesOrm(
                title="Python Разработчик",
                compensation=150000,
                workload=Workload.fulltime,
                worker_id=1,
            )
            worker_2_resume_1 = ResumesOrm(
                title="Python Data Engineer",
                compensation=250000,
                workload=Workload.parttime,
                worker_id=2,
            )
            worker_2_resume_2 = ResumesOrm(
                title="Data Scientist",
                compensation=300000,
                workload=Workload.fulltime,
                worker_id=2,
            )
            session.add_all(
                [
                    worker_1_resume_1,
                    worker_1_resume_2,
                    worker_2_resume_1,
                    worker_2_resume_2,
                ]
            )
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        """
        SELECT workload, AVG(compensation)::INT AS avg_compensation
        FROM resumes
        WHERE title LIKE '%Python%' AND compensation > 40000
        GROUP BY workload
        HAVING AVG(compensation) > 70000
        """
        with session_factory() as session:
            print()
            query = (
                select(
                    ResumesOrm.workload,
                    func.avg(ResumesOrm.compensation)
                    .cast(Integer)
                    .label("avg_compensation"),
                )
                .select_from(ResumesOrm)
                .filter(
                    and_(
                        ResumesOrm.title.contains(like_language),
                        ResumesOrm.compensation > 40000,
                    )
                )
                .group_by(ResumesOrm.workload)
                .having(func.avg(ResumesOrm.compensation) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result)
            print(result[0].avg_compensation)

    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            print()
            worker_3 = WorkersOrm(username="Artem")  # id 3
            worker_4 = WorkersOrm(username="Roman")  # id 4
            worker_5 = WorkersOrm(username="Petr")  # id 5

            resume_5 = ResumesOrm(
                title="Python программист",
                compensation=60000,
                workload="fulltime",
                worker_id=3,
            )
            resume_6 = ResumesOrm(
                title="Machine Learning Engineer",
                compensation=70000,
                workload="parttime",
                worker_id=3,
            )
            resume_7 = ResumesOrm(
                title="Python Data Scientist",
                compensation=80000,
                workload="parttime",
                worker_id=4,
            )
            resume_8 = ResumesOrm(
                title="Python Analyst",
                compensation=90000,
                workload="fulltime",
                worker_id=4,
            )
            resume_9 = ResumesOrm(
                title="Python Junior Developer",
                compensation=100000,
                workload="fulltime",
                worker_id=5,
            )
            data_workers = [worker_3, worker_4, worker_5]
            session.add_all(data_workers)
            session.flush()  # иначе не получается вставить резюме, ведь воркеров еще нет

            data_resumes = [resume_5, resume_6, resume_7, resume_8, resume_9]
            session.add_all(data_resumes)
            session.commit()

    # session.flush() - синхронизирует состояние сессии с БД не завершая транзакцию
    # session.expire() - делает текущие данные объекта устаревшими
    # session.refresh() - немедленно загружает свежие данные из БД
