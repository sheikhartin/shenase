import os
from unittest.mock import Mock

from fastapi.testclient import TestClient

from shenase import models, enums


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
        '/token/', data={'username': 'johndoe', 'password': 'password123'}
    )
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_read_users_me(
    test_client: TestClient,
    create_test_user: models.User,
) -> None:
    login_response = test_client.post(
        '/token/', data={'username': 'johndoe', 'password': 'password123'}
    )
    login_data = login_response.json()
    token = login_data['access_token']
    response = test_client.get(
        '/users/me/', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == 'johndoe'


def test_change_user_role(
    test_client: TestClient,
    create_test_admin_user: models.User,
    create_test_user: models.User,
) -> None:
    login_response = test_client.post(
        '/token/', data={'username': 'adminuser', 'password': 'testpass123'}
    )
    login_data = login_response.json()
    token = login_data['access_token']
    response = test_client.patch(
        '/users/johndoe/role/',
        headers={'Authorization': f'Bearer {token}'},
        params={'new_role': enums.UserRole.MODERATOR},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['role'] == enums.UserRole.MODERATOR


def test_update_user(
    test_client: TestClient,
    create_test_user: models.User,
    mock_save_avatar: Mock,
) -> None:
    login_response = test_client.post(
        '/token/', data={'username': 'johndoe', 'password': 'password123'}
    )
    login_data = login_response.json()
    token = login_data['access_token']

    test_avatar_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'avatar.png'
    )
    with open(test_avatar_file, 'rb') as f:
        response = test_client.patch(
            '/users/me/',
            headers={'Authorization': f'Bearer {token}'},
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
        '/token/', data={'username': 'johndoe', 'password': 'password123'}
    )
    login_data = login_response.json()
    token = login_data['access_token']
    test_avatar_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'avatar.png'
    )
    with open(test_avatar_file, 'rb') as f:
        response = test_client.patch(
            '/users/me/',
            headers={'Authorization': f'Bearer {token}'},
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
