import datetime
import enum
from typing import Annotated

from sqlalchemy import Enum, String, text
from sqlalchemy.orm import DeclarativeBase, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_255 = Annotated[str, 255]

created_at_time = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    ),
]
# server_default - вычисляется на уровне БД
# default - вычисляется на уровне приложения и передается в БД

updated_at_time = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
]
# onupdate - при апдейте записи через ORM, вычисляет и передает в БД


class Base(DeclarativeBase):
    """type_annotation_map хранит сопоставления,
    как type hints должны быть преобразованы в типы SQL в БД при создании таблиц.

        class Workload(enum.Enum):
            ...
        class ResumesOrm(Base):
            ...
            workload: Mapped[Workload]

    Все атрибуты моделей с типом enum.Enum будут преобразованы в ENUM и созданны в БД
    с параметром native_enum=False (универсальная реализация Enum из SQLAlchemy).
    """

    type_annotation_map = {
        str_255: String(255),
        enum.Enum: Enum(native_enum=False),
    }

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")  # type: ignore
        return f"<{self.__class__.__name__}: {', '.join(cols)}>"
