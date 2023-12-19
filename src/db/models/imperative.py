"""Imperative style + Column"""

import datetime

from sqlalchemy import (
    TIMESTAMP,
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    text,
)

from db.models import Workload

metadata_imp = MetaData()


workers_tab = Table(
    "workers",
    metadata_imp,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

resumes_tab = Table(
    "resumes",
    metadata_imp,
    Column("id", Integer, primary_key=True),
    Column("title", String(255)),
    Column("compensation", Integer, nullable=True),
    Column("workload", Enum(Workload)),
    Column("worker_id", ForeignKey("workers.id", ondelete="CASCADE")),  # type: ignore
    Column(
        "created_at",
        TIMESTAMP,
        server_default=text("TIMEZONE('utc', now())"),
    ),
    Column(
        "updated_at",
        TIMESTAMP,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
)
