"""Declarative style + Mapped"""

import enum

from sqlalchemy import CheckConstraint, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base, created_at_time, int_pk, str_255, updated_at_time


#################################### WorkersOrm ####################################
class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[int_pk]
    username: Mapped[str_255]

    resumes: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
    )
    # back_populates используется для указания на обратную сторону отношения.
    # Это позволяет автоматически обновлять обе стороны отношения.

    resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')",
        # order_by="desc(ResumesOrm.id)",
        # lazy="selectin",
    )


#################################### ResumesOrm ####################################
class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[int_pk]
    title: Mapped[str_255]
    compensation: Mapped[int | None]  # or   = mapped_column(nullable=True)
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    # ForeignKey(WorkersOrm.id) - могут быть проблемы с импортами
    # CASCADE - при удалении работника, каскадно удалятся все его резюме
    created_at: Mapped[created_at_time]
    updated_at: Mapped[updated_at_time]

    worker: Mapped["WorkersOrm"] = relationship(
        back_populates="resumes",
    )

    # m_to_m через VacanciesRepliesOrm
    vacancies_replied: Mapped[list["VacanciesOrm"]] = relationship(
        back_populates="resumes_replied",
        secondary="vacancies_replies",
    )

    # primary_keys, foreign_keys, indexes, constraints
    __table_args__ = (
        Index("title_index", "title"),
        CheckConstraint("compensation > 0", name="check_compensation_positive"),
    )


#################################### VacanciesOrm ####################################
class VacanciesOrm(Base):
    __tablename__ = "vacancies"

    id: Mapped[int_pk]
    title: Mapped[str_255]
    compensation: Mapped[int | None]

    # m_to_m через VacanciesRepliesOrm
    resumes_replied: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="vacancies_replied",
        secondary="vacancies_replies",
    )


####################################### M_to_M #######################################
class VacanciesRepliesOrm(Base):
    __tablename__ = "vacancies_replies"

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True,
    )

    cover_letter: Mapped[str | None]
