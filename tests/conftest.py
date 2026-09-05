import os
import sys

_tests_dir = os.path.dirname(os.path.abspath(__file__))
_backend_dir = os.path.abspath(os.path.join(_tests_dir, ".."))
_root_dir = os.path.abspath(os.path.join(_backend_dir, ".."))

if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.core.security import create_access_token

# In-memory SQLite Engine for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Fixture providing an isolated clean database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Fixture providing FastAPI TestClient wired to the test database session."""
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers_factory(client):
    """Factory fixture to register/login a test user and return Authorization headers."""
    def _create_headers(email="testuser@example.com", password="SecurePassword123!", full_name="Test User"):
        register_res = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": full_name,
                "phone_number": "+1234567890"
            }
        )
        user_data = register_res.json()
        user_id = user_data["id"]

        login_res = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password}
        )
        token = login_res.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}, user_data

    return _create_headers

@pytest.fixture
def auth_headers(auth_headers_factory):
    """Convenience fixture returning Authorization headers for a default registered user."""
    headers, _ = auth_headers_factory()
    return headers
