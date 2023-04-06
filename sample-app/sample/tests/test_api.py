from urllib import response
import pytest

from fastapi.testclient import TestClient

from sample.common.config import override_settings

# Override settings
override_settings(
    **{
        "sqlite_url": "sqlite:///./test-sample.sqlite",
        "enable_api_key_validation": False,
    }
)

# Import it later once settings has been overriden
from sample.db.sqlalchemy import get_engine, create_schema
from sample.main import app
from sample.tests import utils

client = TestClient(app)


@pytest.fixture()
def setup_teardown_db():
    utils.create_schema()
    yield
    utils.delete_schema()


def test_root_url():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health": "OK"}