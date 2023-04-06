from contextlib import contextmanager

import logging

from sqlalchemy import asc, desc
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy import and_


from sample.common.exceptions import SampleException, UserAlreadyExists, UserNotFound
from sample.common.utils import retry
from sample.db.sqlalchemy import get_session, models


LOG = logging.getLogger(__name__)
EXCEPTIONS_TO_BE_RETRIED = (OperationalError,)  # Need to be a tupple


def get_backend():
    """The backend is this module itself."""
    return UserRepo()


@contextmanager
def model_query(model, *args, **kwargs):
    """Query helper for simpler session usage."""
    session = get_session()
    try:
        yield session.query(model, *args)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class UserRepo(object):

    def __init__(self):
        self._model_class = models.User

    def _insert_data(self, **model_kwargs):
        """Used in testing, do not expose out side"""
        session = get_session()
        model = self._model_class(**model_kwargs)
        try:
            session.add(model)
            session.commit()
            return model.to_dict()
        except Exception as ex:
            session.rollback()
            LOG.debug(ex)
            raise ex
        finally:
            session.close()

    def _insert_in_batch(self, models):
        session = get_session()
        try:
            session.bulk_insert_mappings(self._model_class, models)
            session.commit()
        except Exception as ex:
            session.rollback()
            raise
        finally:
            session.close()

    def add_user(self, **model_kwargs):
        try:
            return self._insert_data(**model_kwargs)
        except IntegrityError:
            LOG.debug("causgth exception")
            raise UserAlreadyExists()

    def _insert_to_users_in_batch(self, models):
        self._insert_in_batch(models)

    def _add_sorting_and_limit(self, query, sort_key, sort_dir, limit):
        if sort_dir and sort_key:
            sort_dir_func = {
                "asc": asc,
                "desc": desc,
            }[sort_dir]
            sort_key_attr = getattr(self._model_class, sort_key)
            query = query.order_by(sort_dir_func(sort_key_attr))
        if limit is not None:
            query = query.limit(limit)
        return query

    def _add_users_filter(self, query, filters):
        """Add filters to Query"""
        if not filters:
            return query

        filter_names = ["phone", "email"]
        for name in filter_names:
            if name in filters:
                value = filters[name]
                column = getattr(self._model_class, name)
                query = query.filter(column == value)
        return query

    @ retry(exceptions=EXCEPTIONS_TO_BE_RETRIED, logger=LOG)
    def get_all_users(
        self,
        filters=None,
        limit=None,
        sort_key=None,
        sort_dir=None,
    ):

        with model_query(self._model_class) as query:
            query = self._add_users_filter(query, filters)
            query = self._add_sorting_and_limit(query, sort_key, sort_dir, limit)
            model_list = query.all()
            if not model_list:
                raise UserNotFound("No records were found")
            return [model.to_dict() for model in model_list]