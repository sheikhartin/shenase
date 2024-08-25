from sqlalchemy.orm import Session

from shenase import models, schemas, crud


def test_create_user(test_db_session: Session) -> None:
    user_data = schemas.UserCreate(
        username='johndoe',
        email='johndoe@example.com',
        password='password123',
        display_name='John Doe',
    )
    user = crud.create_user(db=test_db_session, user=user_data)
    assert user.username == 'johndoe'
    assert user.email == 'johndoe@example.com'


def test_get_user(
    test_db_session: Session,
    create_test_user: models.User,
) -> None:
    user = crud.get_user(db=test_db_session, user_id=1)
    assert user is not None
    assert user.username == 'johndoe'


def test_get_user_by_username(
    test_db_session: Session,
    create_test_user: models.User,
) -> None:
    user = crud.get_user_by_username(db=test_db_session, username='johndoe')
    assert user is not None
    assert user.username == 'johndoe'


def test_get_user_by_email(
    test_db_session: Session,
    create_test_user: models.User,
) -> None:
    user = crud.get_user_by_email(
        db=test_db_session, email='johndoe@example.com'
    )
    assert user is not None
    assert user.email == 'johndoe@example.com'
