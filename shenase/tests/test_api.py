import os
from unittest.mock import Mock

from fastapi.testclient import TestClient

from shenase import models


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
    test_client: TestClient, create_test_user: models.User
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
        response = test_client.post(
            '/users/avatar/',
            headers={'Authorization': f'Bearer {token}'},
            files={
                'file': (
                    'avatar.png',
                    f,
                    'image/png',
                )
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data['response_message'] == 'Avatar uploaded successfully.'
    assert 'file_location' in data
