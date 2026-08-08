import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ads.models import Advertisement
from users.models import CustomUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        email="testadduser@gmail.com",
        password="testaddduser",
        first_name="test",
        last_name="adduser",
        phone="88003837363",
    )


@pytest.fixture
def second_user(db):
    return CustomUser.objects.create_user(
        email="secondtestadduser@gmail.com",
        password="secondtestaddduser",
        first_name="secondtest",
        last_name="adduser",
        phone="88002783726",
    )


@pytest.fixture
def ad(db, user):
    return Advertisement.objects.create(
        title="test_add",
        price=100,
        description="test_description",
        author=user,
    )


@pytest.fixture
def second_ad(db, second_user):
    return Advertisement.objects.create(
        title="test_add2",
        price=1002,
        description="test_description2",
        author=second_user,
    )


@pytest.mark.django_db
class TestAdvertisementAPI:

    def test_current_user_ads(self, api_client, user, ad, second_ad):
        """Тесты с объявлениями текущего пользователя"""

        # Тест просмотра чужого объявления без авторизации
        url_retrieve = reverse("ads:ad-detail", kwargs={"pk": ad.pk})
        retrieve_response = api_client.get(url_retrieve)
        assert retrieve_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Тест получения списка объявлений
        url_list = reverse("ads:ad-list")
        api_client.force_authenticate(user=user)
        response_list = api_client.get(url_list)
        assert response_list.status_code == status.HTTP_200_OK
        assert len(response_list.json()["results"]) == 2

        # Тест создания нового объявления
        url_create = reverse("ads:ad-list")
        response_create = api_client.post(url_create, data={
            "title": "testcreate",
            "price": 500,
            "description": "test_create",
            "author": user.pk,
        })
        assert response_create.status_code == status.HTTP_201_CREATED
        assert Advertisement.objects.filter(title="testcreate").exists()

        url_detail = reverse("ads:ad-detail", kwargs={"pk": ad.pk})

        # Тест получения одного объявления
        response_detail = api_client.get(url_detail)
        assert response_detail.status_code == status.HTTP_200_OK
        assert response_detail.json()["title"] == "test_add"

        # Тест изменения объявления
        response_patch = api_client.patch(url_detail, data={"title": "testpatch"})
        assert response_patch.status_code == status.HTTP_200_OK
        assert Advertisement.objects.filter(title="testpatch").exists()

        # Тест удаления объявления
        response_delete = api_client.delete(url_detail)
        assert response_delete.status_code == status.HTTP_204_NO_CONTENT

    def test_other_user_ads(self, api_client, second_ad):
        """Тест попытки обновить/удалить чужое объявление"""

        url_update = reverse("ads:ad-detail", kwargs={"pk": second_ad.pk})

        patch_response = api_client.patch(url_update, data={"title": "test_patch"})
        assert patch_response.status_code == status.HTTP_401_UNAUTHORIZED

        put_response = api_client.put(url_update, data={
            "title": "test_put",
            "price": 500,
            "description": "testput",
        })
        assert put_response.status_code == status.HTTP_401_UNAUTHORIZED

        delete_response = api_client.delete(url_update)
        assert delete_response.status_code == status.HTTP_401_UNAUTHORIZED