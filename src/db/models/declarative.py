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

    # primary_keys, foreign_keys, indexes, constraints
    __table_args__ = (
        Index("title_index", "title"),
        CheckConstraint("compensation > 0", name="check_compensation_positive"),
    )
