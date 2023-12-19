from sqlalchemy import Integer, and_, func, insert, select, text, update

from db.engine import engine
from db.models import Workload, metadata_imp, resumes_tab, workers_tab


class SyncCore:
    @staticmethod
    def get_version():
        with engine.connect() as conn:
            stmt = "SELECT VERSION()"
            res = conn.execute(text(stmt))
            print("sync_version=", res.all(), sep="")

    @staticmethod
    def delete_tables():
        engine.echo = False
        metadata_imp.drop_all(engine)
        engine.echo = True

    @staticmethod
    def create_tables():
        print()
        metadata_imp.create_all(engine)