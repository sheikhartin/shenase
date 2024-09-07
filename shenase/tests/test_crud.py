from sqlalchemy.orm import Session

from shenase import models, schemas, crud, enums


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


def test_update_user(
    test_db_session: Session,
    create_test_user: models.User,
) -> None:
    user_update = schemas.UserProfileUpdate(
        username='updateduser',
        email='updateduser@example.com',
        password='newpassword123',
        display_name='Updated User',
        bio='Updated bio.',
        location='Updated location.',
    )
    updated_user = crud.update_user(
        db=test_db_session,
        user=user_update,
        current_user=create_test_user,
    )

    assert updated_user.username == 'updateduser'
    assert updated_user.email == 'updateduser@example.com'
    assert updated_user.profile.display_name == 'Updated User'
    assert updated_user.profile.bio == 'Updated bio.'
    assert updated_user.profile.location == 'Updated location.'


def test_get_user(
    test_db_session: Session,
    create_test_user: models.User,
) -> None:
    user = crud.get_user_by_id(db=test_db_session, user_id=1)
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


def test_update_user_role(
    test_db_session: Session,
    create_test_user: models.User,
) -> None:
    updated_user = crud.update_user_role(
        db=test_db_session,
        username='johndoe',
        new_role=enums.UserRole.MODERATOR,
    )
    assert updated_user.role == enums.UserRole.MODERATOR


def test_update_user_status(
    test_db_session: Session,
    create_test_user: models.User,
) -> None:
    updated_user = crud.update_user_status(
        db=test_db_session,
        username='johndoe',
        new_status=enums.UserStatus.SUSPENDED,
    )
    assert updated_user.status == enums.UserStatus.SUSPENDED
