from sqlalchemy import Integer, and_, func, select
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from db import Base
from db.engine import engine, session_factory
from db.models import ResumesOrm, WorkersOrm, Workload


class SyncOrm:
    pass
