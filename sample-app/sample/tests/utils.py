from sample.db import api
from sample.db import base


def delete_schema():
    base.base_model.Base.metadata.drop_all(bind=base.get_engine())


def create_schema():
    base.create_schema()


def create_user(name, phone, email):
    model = {
        "name": name,
        "phone": phone,
        "email": email
    }
    api.add_user(model)


def create_users(user_list):
    for name, phone, email in user_list:
        create_user(name, phone, email)
