import logging

from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from sample.common.config import get_settings


LOG = logging.getLogger(__name__)

_SQL_ENGINE_FACADE = None


class SqlEngineFacade:
    def __init__(self, **engine_kwargs):
        self._session_maker = None
        self._engine = None
        self._engine_kwargs = engine_kwargs

    def _get_uri(self):
        settings = get_settings()
        if settings.db_host and settings.db_port and settings.db_name and settings.db_user:
            db_name = settings.db_name
            db_host = settings.db_host
            db_port = settings.db_port
            db_user = settings.db_user
            DATABASE_URL = engine.url.URL.create(
                drivername="mysql+pymysql",
                host=db_host,
                port=db_port,
                database=db_name,
                username=db_user
        )
        else:
            DATABASE_URL = get_settings().sqlite_url
        return DATABASE_URL


    def get_engine(self):
        if self._engine is None:
            uri = self._get_uri()
            self._engine = create_engine(uri, echo=True, **self._engine_kwargs)
        return self._engine

    def get_session(self, autocommit=False, autoflush=False, expire_on_commit=False):
        if self._session_maker is None:
            self._session_maker = scoped_session(
                sessionmaker(
                    bind=self.get_engine(),
                    autoflush=autoflush,
                    autocommit=autocommit,
                    expire_on_commit=expire_on_commit,
                )
            )
        return self._session_maker


def _create_sql_facade():
    global _SQL_ENGINE_FACADE
    if _SQL_ENGINE_FACADE is None:
        _SQL_ENGINE_FACADE = SqlEngineFacade()
    return _SQL_ENGINE_FACADE


def create_schema():
    engine = get_engine()
    from sample.db.sqlalchemy.models import Base

    LOG.info("Creating Tables")
    Base.metadata.create_all(engine)


def get_session():
    facade = _create_sql_facade()
    return facade.get_session()


def get_engine():
    facade = _create_sql_facade()
    return facade.get_engine()
