import os

os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "postgresql+psycopg://localhost/townhall_test")

import pytest
from fastapi.testclient import TestClient

from app.db import Base, engine
from app.main import app


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestClient(app) as c:
        yield c
