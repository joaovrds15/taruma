import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_login_with_invalid_credentials(api_client):

    url = reverse('login')
    data = {
        'username': 'joaoteste',
        'password': 'credentialsPass',
    }
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    assert response.status_code == 401
    assert "No active account found with the given credentials" in message


@pytest.mark.django_db
def test_login_with_valid_credentials(api_client):
    user = User.objects.create_user(username='testuser', password='testpass')
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'testpass',
    }
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    assert response.status_code == 200
    assert 'token' in message


@pytest.mark.django_db
def test_register_with_valid_data(api_client):

    url = reverse('register')
    data = {
        'username': 'joaoteste',
        'password': 'credentialsPass',
        'first_name': "joao",
        'last_name': 'victor',
    }
    response = api_client.post(url, data=data,  format='json')
    message = response.content.decode('utf-8')
    assert response.status_code == 201
    assert "User Created Successfully" in message


@pytest.mark.django_db
def test_register_when_username_already_taken(api_client):

    url = reverse('register')
    user = User.objects.create_user(
        username='joaoteste',
        password='credentialsPass',
        first_name="joao",
        last_name='victor',
    )
    data = {
        'username': 'joaoteste',
        'password': 'credentialsPass',
        'first_name': "joao",
        'last_name': 'victor',
    }
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    assert response.status_code == 400
    assert "A user with that username already exists." in message
