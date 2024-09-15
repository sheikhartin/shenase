import os
from unittest.mock import Mock

from fastapi.testclient import TestClient

from shenase import models, enums
from shenase.config import DEFAULT_AVATAR


def test_create_user(test_client: TestClient) -> None:
    response = test_client.post(
        '/users/',
        data={
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'display_name': 'John Doe',
            'bio': 'This is a test bio for John Doe.',
            'location': 'New York',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == 'johndoe'
    assert 'id' in data


def test_login_user(
    test_client: TestClient,
    create_test_user: models.User,
) -> None:
    response = test_client.post(
        '/login/', json={'username': 'johndoe', 'password': 'password123'}
    )
    assert response.status_code == 200
    assert 'user_id' in response.cookies


def test_read_users_me(
    test_client: TestClient,
    create_test_user: models.User,
    mock_middlewares_get_db: Mock,
) -> None:
    login_response = test_client.post(
        '/login/', json={'username': 'johndoe', 'password': 'password123'}
    )
    user_id = login_response.cookies.get('user_id')
    test_client.cookies.set('user_id', user_id)
    response = test_client.get('/users/me/')
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == 'johndoe'


def test_get_user_profile(
    test_client: TestClient,
    create_test_user: models.User,
) -> None:
    response = test_client.get(f'/users/{create_test_user.username}/profile/')
    assert response.status_code == 200
    data = response.json()
    assert data['display_name'] == 'John Doe'
    assert data['avatar'] == DEFAULT_AVATAR
    assert data['bio'] is None
    assert data['location'] is None


def test_change_user_role(
    test_client: TestClient,
    create_test_admin_user: models.User,
    create_test_user: models.User,
) -> None:
    login_response = test_client.post(
        '/login/', json={'username': 'adminuser', 'password': 'testpass123'}
    )
    user_id = login_response.cookies.get('user_id')
    test_client.cookies.set('user_id', user_id)
    response = test_client.patch(
        '/users/johndoe/role/',
        params={'new_role': enums.UserRole.MODERATOR},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['role'] == enums.UserRole.MODERATOR


def test_change_user_status(
    test_client: TestClient,
    create_test_admin_user: models.User,
    create_test_user: models.User,
) -> None:
    login_response = test_client.post(
        '/login/', json={'username': 'adminuser', 'password': 'testpass123'}
    )
    user_id = login_response.cookies.get('user_id')
    test_client.cookies.set('user_id', user_id)
    response = test_client.patch(
        '/users/johndoe/status/',
        params={'new_status': enums.UserStatus.INACTIVE},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == enums.UserStatus.INACTIVE


def test_update_user(
    test_client: TestClient,
    create_test_user: models.User,
    mock_save_avatar: Mock,
) -> None:
    login_response = test_client.post(
        '/login/', json={'username': 'johndoe', 'password': 'password123'}
    )
    user_id = login_response.cookies.get('user_id')
    test_client.cookies.set('user_id', user_id)

    test_avatar_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'avatar.png'
    )
    with open(test_avatar_file, 'rb') as f:
        response = test_client.patch(
            '/users/me/',
            data={
                'username': 'updateduser',
                'display_name': 'Updated User',
            },
            files={
                'avatar': (
                    'avatar.png',
                    f,
                    'image/png',
                )
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == 'updateduser'
    assert data['profile']['display_name'] == 'Updated User'
    assert data['profile']['avatar'] == 'mocked_avatar_path.png'


def test_upload_avatar(
    test_client: TestClient,
    create_test_user: models.User,
    mock_save_avatar: Mock,
) -> None:
    login_response = test_client.post(
        '/login/', json={'username': 'johndoe', 'password': 'password123'}
    )
    user_id = login_response.cookies.get('user_id')
    test_client.cookies.set('user_id', user_id)
    test_avatar_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'avatar.png'
    )
    with open(test_avatar_file, 'rb') as f:
        response = test_client.patch(
            '/users/me/',
            files={
                'avatar': (
                    'avatar.png',
                    f,
                    'image/png',
                )
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data['profile']['avatar'] == 'mocked_avatar_path.png'
