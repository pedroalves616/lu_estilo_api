import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.session import Base, get_db
from app.database.models import User
from app.core.security import get_password_hash
from app.core.config import settings


SQLALCHEMY_DATABASE_URL = "postgresql://test_user:test_password@localhost:5433/test_lu_estilo_db" 


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine) 
    yield engine
    Base.metadata.drop_all(bind=engine) 

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback() 
    connection.close()

@pytest.fixture(scope="function")
def override_get_db(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def client(override_get_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="function")
def test_user(db_session):
    hashed_password = get_password_hash("testpassword")
    user = User(username="testuser", email="test@example.com", hashed_password=hashed_password, role="regular")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_admin_user(db_session):
    hashed_password = get_password_hash("adminpassword")
    admin_user = User(username="adminuser", email="admin@example.com", hashed_password=hashed_password, role="admin")
    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)
    return admin_user

@pytest.fixture(scope="function")
async def regular_user_token(client, test_user):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    return response.json()["access_token"]

@pytest.fixture(scope="function")
async def admin_user_token(client, test_admin_user):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "adminuser", "password": "adminpassword"}
    )
    return response.json()["access_token"]