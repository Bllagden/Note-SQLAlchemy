from sqlalchemy import Integer, and_, func, select
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from db import Base
from db.engine import engine, session_factory
from db.models import ResumesOrm, VacanciesOrm, WorkersOrm, Workload
from schemas import (
    ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO,
    WorkersDTO,
    WorkersRelDTO,
    WorkloadAvgCompensationDTO,
)


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

    @staticmethod
    def join_cte_subquery_window_func():
        """
        WITH helper2 AS (
            SELECT *, compensation-avg_workload_compensation AS compensation_diff
            FROM
            (SELECT
                w.id,
                w.username,
                r.compensation,
                r.workload,
                avg(r.compensation) OVER (PARTITION BY workload)::INT AS avg_workload_compensation
            FROM resumes r
            JOIN workers w ON r.worker_id = w.id) helper1
        )
        SELECT * FROM helper2
        ORDER BY compensation_diff DESC;

        CTE - временные именованные результаты запросов (helper1, helper2).

        Оконная функция - avg(r.compensation) OVER (PARTITION BY workload)::INT AS avg...
        Выполняет вычисления для каждого подмножества строк.
        В данном случае считает среднее compensation для разных workload (part, full).
        """
        with session_factory() as session:
            print()
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation)  # type: ignore
                    .over(partition_by=r.workload)
                    .cast(Integer)
                    .label("avg_workload_compensation"),
                )
                .select_from(r)  # можно не указывать (алхимия поймет)
                .join(w, r.worker_id == w.id)
                .subquery("helper1")
            )
            cte = select(
                subq.c.worker_id,
                subq.c.username,
                subq.c.compensation,
                subq.c.workload,
                subq.c.avg_workload_compensation,
                (subq.c.compensation - subq.c.avg_workload_compensation).label(
                    "compensation_diff"
                ),
            ).cte("helper2")
            query = select(cte).order_by(cte.c.compensation_diff.desc())

            res = session.execute(query)
            result = res.all()
            print()
            print(f"{len(result)=}\n{result=}")

    ############################### RELATIONSHIP ###############################
    # Для каких связей типы загрузок
    # joinedload    : m_to_1,    1_to_1
    # selectinload  : 1_to_m,    m_to_m

    @staticmethod
    def select_workers_lazy_relationship():
        """lazy (ленивая) загрузка (дефолт).
        Работает только в синхронном режиме.
        Сначала делается запрос для выборки изначальных данных (воркеров).
        Связанные данные (резюме воркеров) загружаются по запросу (workers[?].resumes).
        Неэффективно, если все связанные данные нужно получить разом (будет n+1 запросов).
        """
        with session_factory() as session:
            print()

            query = select(WorkersOrm).order_by(WorkersOrm.id)  # desc(WorkersOrm.id)
            res = session.execute(query)  # SELECT * FROM workers
            workers = res.scalars().all()  # list[Orm[id=?, username=?]]
            print(f"{workers=}")

            worker_1_resumes = workers[0].resumes  # запрос всех резюме воркера с id=1
            print(f"{worker_1_resumes=}")

            worker_2_resumes = workers[1].resumes  # запрос всех резюме воркера с id=2
            print(f"{worker_2_resumes=}")

    @staticmethod
    def select_workers_joined_relationship():
        """joined загрузка.
        К SELECT запросу добавляется JOIN для выборки связанных данных.
        В результат попадают дубликаты (сколько резюме у воркера, столько и его дубликатов).
        Алхимия будет ругаться на дубликаты первичных ключей, поэтому на уровне питона
        их нужно удалить из результата методом unique().
        Один большой запрос, вместо n+1 запросов в ленивой загрузке.
        Слишком много лишних данных берется из БД из-за ДЖОЙНА (дубликаты).
        """
        with session_factory() as session:
            print()

            query = select(WorkersOrm).options(joinedload(WorkersOrm.resumes))
            res = session.execute(query)  # SELECT с джойном
            workers = res.unique().scalars().all()  # удаление дубликатов
            print(f"{workers=}")

            worker_1_resumes = workers[0].resumes  # здесь нет запроса
            print(f"{worker_1_resumes=}")

            worker_2_resumes = workers[1].resumes  # здесь нет запроса
            print(f"{worker_2_resumes=}")

    @staticmethod
    def select_workers_selectin_relationship():
        """selectin загрузка.
        Два запроса:
        первый - все воркеры; второй - все резюме выбранных воркеров.
        Нет дубликатов воркеров.
        """
        with session_factory() as session:
            print()

            query = (
                select(WorkersOrm)
                .order_by(WorkersOrm.id)
                .options(selectinload(WorkersOrm.resumes))
            )
            res = session.execute(query)
            workers = res.scalars().all()
            print(f"{workers=}")

            worker_1_resumes = workers[0].resumes
            print(f"{worker_1_resumes=}")

            worker_2_resumes = workers[1].resumes
            print(f"{worker_2_resumes=}")

    @staticmethod
    def select_worker_selectin_relationship(worker_id: int = 1):
        with session_factory() as session:
            print()
            query = (
                select(WorkersOrm)
                .filter_by(id=worker_id)
                .options(selectinload(WorkersOrm.resumes))
            )
            res = session.execute(query)
            # type(res) = sqlalchemy.engine.result.ChunkedIteratorResult

            # worker = res.scalars()  # sqlalchemy.engine.result.ScalarResult
            # worker = res.scalars().all()  # list[db...WorkersOrm]
            # worker = res.scalars().all()[0]  # db.models.declarative.WorkersOrm
            worker = res.scalars().first()  # db.models.declarative.WorkersOrm | None

            if worker:
                print(f"{worker=}")
                print(f"{worker.resumes=}")
            else:
                print("worker not found")

    ##########################################################################

    @staticmethod
    def select_workers_condition_relationship():
        """Выбор всех воркеров и их резюме (резюме только с parttime).
        WorkersOrm.resumes_parttime (primaryjoin).
        """
        with session_factory() as session:
            print()

            query = (
                select(WorkersOrm)
                .order_by(WorkersOrm.id)
                .options(selectinload(WorkersOrm.resumes_parttime))
            )
            res = session.execute(query)
            workers = res.scalars().all()
            print(f"{workers=}")

            worker_1_resumes = workers[0].resumes_parttime
            print(f"{worker_1_resumes=}")

            worker_2_resumes = workers[1].resumes_parttime
            print(f"{worker_2_resumes=}")

    @staticmethod
    def select_workers_condition_relationship_contains_eager():
        """Eager загрузка.
        Возвращает только тех воркеров, у которых есть рюзюме с parttime.
        При текущем варианте, делает два запроса. Но вообще предназначена делать один.
        Реализовано в асинхронном варианте функции.
        """
        with session_factory() as session:
            print()
            query = (
                select(WorkersOrm)
                .join(WorkersOrm.resumes)
                .options(contains_eager(WorkersOrm.resumes))
                .filter(ResumesOrm.workload == "parttime")
            )

            res = session.execute(query)
            workers = res.unique().scalars().all()
            print(f"{workers=}")

            worker_1_resumes = workers[0].resumes_parttime
            print(f"{worker_1_resumes=}")

    @staticmethod
    def select_workers_relationship_contains_eager_with_limit():
        """Eager загрузка с лимитом выдачи.
        Возвращает всех воркеров и определенное количество резюме у каждого.
        https://stackoverflow.com/a/72298903/22259413
        """
        with session_factory() as session:
            print()
            subq = (
                select(ResumesOrm.id.label("resume_id"))
                .filter(ResumesOrm.worker_id == WorkersOrm.id)
                .limit(1)  # количество резюме у каждого воркера
                .scalar_subquery()
                .correlate(WorkersOrm)
            )

            query = (
                select(WorkersOrm)
                .order_by(WorkersOrm.id)
                .join(ResumesOrm, ResumesOrm.id.in_(subq))
                .options(contains_eager(WorkersOrm.resumes))
            )

            res = session.execute(query)
            workers = res.unique().scalars().all()
            print(f"{workers=}")

            worker_1_resumes = workers[0].resumes
            print(f"{worker_1_resumes=}")

            worker_2_resumes = workers[1].resumes
            print(f"{worker_2_resumes=}")

    ################################### DTO ###################################

    @staticmethod
    def convert_workers_to_dto():
        """Воркеры (pydantic модель)"""
        with session_factory() as session:
            print()

            query = select(WorkersOrm).order_by(WorkersOrm.id).limit(3)
            res = session.execute(query)
            workers_orm = res.scalars().all()
            print(f"{workers_orm=}")

            # приведение данных к pydantic модели
            workers_dto = [
                WorkersDTO.model_validate(row, from_attributes=True)
                for row in workers_orm
            ]
            # from_attributes=True - для orm объектов (обращение к атрибутам через точку),
            # а не по ключам словаря
            print(f"{workers_dto=}")

    @staticmethod
    def convert_workers_to_dto_with_rel():
        """Воркеры с вложенными резюме (pydantic модель)"""
        with session_factory() as session:
            print()

            query = (
                select(WorkersOrm)
                .order_by(WorkersOrm.id)
                .options(selectinload(WorkersOrm.resumes))
                .limit(4)
            )
            res = session.execute(query)
            workers_orm = res.scalars().all()
            print(f"{workers_orm=}")

            workers_dto = [
                WorkersRelDTO.model_validate(row, from_attributes=True)
                for row in workers_orm
            ]
            print(f"{workers_dto=}")
            return workers_dto

    @staticmethod
    def convert_workers_to_dto_with_dto_join(like_language: str = "Python"):
        """Старый запрос select_resumes_avg_compensation приведенный к pydantic модели"""
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
            res = session.execute(query)
            result_orm = res.all()
            print(f"{result_orm=}")
            result_dto = [
                WorkloadAvgCompensationDTO.model_validate(row, from_attributes=True)
                for row in result_orm
            ]
            print(f"{result_dto=}")

    ################################### M_to_M ###################################

    @staticmethod
    def add_vacancies_and_replies():
        with session_factory() as session:
            print()
            new_vacancy = VacanciesOrm(title="Python разработчик", compensation=100000)

            # query = select(ResumesOrm).filter_by(id=1)
            # res = session.execute(query)
            # resume_1 = res.scalars().first()  # db.models.declarative.ResumesOrm
            # or
            resume_1 = session.get(ResumesOrm, 1)  # db.models.declarative.ResumesOrm
            resume_2 = session.get(ResumesOrm, 2)

            # insert
            if resume_1 is not None:
                resume_1.vacancies_replied.append(new_vacancy)
            if resume_2 is not None:
                resume_2.vacancies_replied.append(new_vacancy)

            session.commit()

    @staticmethod
    def select_resumes_with_all_relationships():
        """Выбор всех резюме с вложенными данными (воркер этого рюзюме и вакансии)"""
        with session_factory() as session:
            print()
            query = (
                select(ResumesOrm)
                .options(joinedload(ResumesOrm.worker))  # m_to_1
                .options(  #                               m_to_m
                    selectinload(ResumesOrm.vacancies_replied).load_only(
                        VacanciesOrm.title
                    )
                )
            )

            res = session.execute(query)
            result_orm = res.unique().scalars().all()
            print(f"{result_orm=}")

            result_dto = [
                ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO.model_validate(
                    row, from_attributes=True
                )
                for row in result_orm
            ]
            print(f"{result_dto=}")
            return result_dto
