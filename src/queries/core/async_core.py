from sqlalchemy import Integer, and_, func, insert, select, text, update

from db.engine import async_engine
from db.models import Workload, metadata_imp, resumes_tab, workers_tab


class AsyncCore:
    pass
