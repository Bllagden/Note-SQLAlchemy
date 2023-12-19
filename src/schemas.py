"""DTO (Data Transfer Object) - это шаблон проектирования для передачи данных
между подсистемами приложения. Не содержит поведения и используется для упрощения обмена
информацией между различными уровнями приложения.

Реализован через Pydantic схемы."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from db.models import Workload


class WorkersAddDTO(BaseModel):
    # POST запрос
    username: str


class WorkersDTO(WorkersAddDTO):
    # GET запрос
    id: int


class ResumesAddDTO(BaseModel):
    # POST запрос
    title: str
    compensation: Optional[int]
    workload: Workload
    worker_id: int


class ResumesDTO(ResumesAddDTO):
    # GET запрос
    id: int
    created_at: datetime
    updated_at: datetime


class ResumesRelDTO(ResumesDTO):
    # relationship
    worker: "WorkersDTO"


class WorkersRelDTO(WorkersDTO):
    # relationship
    resumes: list["ResumesDTO"]


class WorkloadAvgCompensationDTO(BaseModel):
    workload: Workload
    avg_compensation: int

    class Config:
        """from_attributes=True - сериализация данных в модель Pydantic для orm объектов
        (обращение к атрибутам через точку, а не по ключам словаря)."""

        #    from_attributes = True
        pass
