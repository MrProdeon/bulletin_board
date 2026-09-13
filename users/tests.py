import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import CustomUser

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        email="testuser1@gmail.com",
        password="testuser1",
        first_name="test",
        last_name="user1",
        phone="88005553535",
    )


@pytest.fixture
def admin(db):
    return CustomUser.objects.create_user(
        email="admin@gmail.com",
        password="admin",
        first_name="test",
        last_name="admin",
        phone="89377012108",
    )


@pytest.fixture
def djoser_user(db):
    return CustomUser.objects.create_user(
        email="testdjoser@gmail.com",
        password="ultrahardpassword",
        first_name="test",
        last_name="user1",
        phone="88003438383",
    )


@pytest.mark.django_db
class TestCustomUserAPI:

    def test_users_list(self, api_client, user):
        url = reverse("users:user-list")

        # Запрет без авторизации
        unauth_response = api_client.get(url)
        assert unauth_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Успех с авторизацией
        api_client.force_authenticate(user=user)
        auth_response = api_client.get(url)
        assert auth_response.status_code == status.HTTP_200_OK

        # Успешное создание юзера при авторизации
        create_response = api_client.post(url, data={
            "email": "test_create@mail.ru",
            "first_name": "test",
            "last_name": "create",
            "phone": "88005554343",
            "password": "testcreatepassword",
        })
        assert create_response.status_code == status.HTTP_201_CREATED
        assert create_response.json()["email"] == "test_create@mail.ru"

    def test_users_detail(self, api_client, user):
        url = reverse("users:user-detail", kwargs={"pk": user.pk})

        # Запрет без авторизации
        unauth_response = api_client.get(url)
        assert unauth_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Успех получения юзера с авторизацией
        api_client.force_authenticate(user=user)
        auth_response = api_client.get(url)
        assert auth_response.status_code == status.HTTP_200_OK
        assert auth_response.json()["email"] == "testuser1@gmail.com"

        # Успешное изменение через PUT
        put_response = api_client.put(url, data={
            "email": "testput@mail.ru",
            "first_name": "test",
            "last_name": "put",
            "phone": "88005553232",
            "password": "testput",
        })
        assert put_response.status_code == status.HTTP_200_OK
        assert put_response.json()["email"] == "testput@mail.ru"

        # Успешное изменение через PATCH
        patch_response = api_client.patch(url, data={"email": "testpatch@mail.ru"})
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.json()["email"] == "testpatch@mail.ru"

        # Успешное удаление через DELETE
        delete_response = api_client.delete(url)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT


# Djoser / JWT

@pytest.mark.django_db
class TestDjoserAPI:

    def test_djoser_register(self, api_client):
        url = reverse("customuser-list")
        data = {
            "email": "testdjoser@mail.com",
            "first_name": "test",
            "last_name": "djoser",
            "phone": "88005556767",
            "password": "veryhardpassword",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert CustomUser.objects.filter(email="testdjoser@mail.com").exists()

    def test_jwt_create(self, api_client):
        CustomUser.objects.create_user(
            email="testdjoser@mail.com",
            first_name="test",
            last_name="djoser",
            phone="88005556767",
            password="veryhardpassword",
        )
        url = reverse("jwt-create")
        data = {"email": "testdjoser@mail.com", "password": "veryhardpassword"}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["refresh"]
        assert response.json()["access"]

    def test_jwt_current_user(self, api_client, djoser_user):
        api_client.force_authenticate(user=djoser_user)
        url = reverse("customuser-me")

        # Получение текущего пользователя
        get_response = api_client.get(url)
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["email"] == "testdjoser@gmail.com"

        # Изменение текущего пользователя
        patch_response = api_client.patch(url, data={"email": "testpatch@mail.ru"})
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.json()["email"] == "testpatch@mail.ru"