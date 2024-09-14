import os
from urllib.parse import urlparse
from unittest.mock import Mock, patch
from typing import Optional, Generator, Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from shenase import models, schemas, crud, enums
from shenase.main import app
from shenase.database import Base
from shenase.dependencies import get_db
from shenase.config import TEST_DATABASE_URL

engine = create_engine(
    TEST_DATABASE_URL, connect_args={'check_same_thread': False}
)
TestingSessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False
)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='function')
def test_db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    nested = connection.begin_nested()

    @event.listens_for(session, 'after_transaction_end')
    def reset_transaction(
        session: Session,
        transaction: Optional[Any],
    ) -> None:
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def test_client(
    test_db_session: Session,
) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield test_db_session
        finally:
            test_db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope='function')
def create_test_admin_user(
    test_db_session: Session,
    mock_middlewares_get_db: Mock,
) -> models.User:
    user_data = schemas.UserCreate(
        username='adminuser',
        email='adminuser@example.com',
        password='testpass123',
        display_name='Admin User',
    )
    with patch('shenase.models.uuid.uuid4') as mock_uuid:
        mock_uuid.return_value.hex = 'admin_id'
        crud.create_user(db=test_db_session, user=user_data)
    return crud.update_user_role(
        db=test_db_session,
        username='adminuser',
        new_role=enums.UserRole.ADMIN,
    )


@pytest.fixture(scope='function')
def create_test_user(
    test_db_session: Session,
    mock_middlewares_get_db: Mock,
) -> models.User:
    user_data = schemas.UserCreate(
        username='johndoe',
        email='johndoe@example.com',
        password='password123',
        display_name='John Doe',
    )
    with patch('shenase.models.uuid.uuid4') as mock_uuid:
        mock_uuid.return_value.hex = 'test_id'
        return crud.create_user(db=test_db_session, user=user_data)


@pytest.fixture(scope='function')
def mock_middlewares_get_db(
    test_db_session: Session,
) -> Generator[Mock, None, None]:
    def get_test_db() -> Generator[Session, None, None]:
        yield test_db_session

    with patch('shenase.middlewares.get_db') as mock_get_db:
        mock_get_db.side_effect = get_test_db
        yield mock_get_db


@pytest.fixture(scope='session')
def mock_save_avatar() -> Generator[Mock, None, None]:
    with patch('shenase.crud.save_avatar') as mock_save_avatar:
        mock_save_avatar.return_value = 'mocked_avatar_path.png'
        yield mock_save_avatar


@pytest.fixture(scope='session', autouse=True)
def teardown_test_database() -> Generator[None, None, None]:
    yield

    Base.metadata.drop_all(bind=engine)

    parsed_url = urlparse(TEST_DATABASE_URL)
    if parsed_url.scheme in ('sqlite',):
        db_file_path = parsed_url.path.strip('/')
        if os.path.exists(db_file_path):
            os.remove(db_file_path)
            print(f'Removed test database file: {db_file_path}')
        else:
            print(f'Test database file does not exist: {db_file_path}')
