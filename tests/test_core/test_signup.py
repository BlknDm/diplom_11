import pytest
from django.urls import reverse
from rest_framework import status

from tests.test_core.factories import SignUpRequest
from todolist.core.models import User


@pytest.mark.django_db()
class TestSignupView:
    url = reverse('todolist.core:signup')

    def test_user_created(self, client):
        data = SignUpRequest.build()

        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get()
        assert response.json() == _serialize_response(user)
        assert user.check_password(data['password'])

    def test_password_invalid(self, client, faker):
        data = SignUpRequest.build(password_repeat=faker.password())

        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'password_repeat': ['Password must match']}

    @pytest.mark.parametrize(
        'password',
        ['1234567890', 'q1w2e', '12345qwerty'],
        ids=['only digits', 'too short', 'too common']
    )
    def test_password_to_lite(self, client, password):
        data = SignUpRequest.build(password=password, password_repeat=password)
        response = client.post(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_already_exists(self, client, user):
        data = SignUpRequest.build(username=user.username)

        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'username': ['Пользователь с таким именем уже существует.']}


def _serialize_response(user: User, **kwargs) -> dict:
    data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    data |= kwargs #update
    return data
