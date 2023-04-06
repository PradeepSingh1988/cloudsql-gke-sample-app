import sys

from sample.db.sqlalchemy import create_schema


def import_module(import_str):
    """Import a module."""
    __import__(import_str)
    return sys.modules[import_str]



DB_DRIVER = import_module("sample.db.sqlalchemy.api").get_backend()

# TODO move it to alembic
create_schema()


def _get_dbdriver_instance():
    """Return a DB API instance."""
    return DB_DRIVER

def add_user(model_kwargs):
    return _get_dbdriver_instance().add_user(**model_kwargs)

def get_all_users(filters=None, limit=None, sort_key=None, sort_dir=None):
    return _get_dbdriver_instance().get_all_users(filters, limit, sort_key, sort_dir)


