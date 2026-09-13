import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from reviews.models import Review
from ads.models import Advertisement
from users.models import CustomUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        email="testuserreview@gmail.com",
        password="testuserreview",
        first_name="testreview",
        last_name="user1",
        phone="88005559835",
    )


@pytest.fixture
def ad(db, user):
    return Advertisement.objects.create(
        title="test_add_review",
        price=1000,
        description="test_description_review",
        author=user,
    )


@pytest.fixture
def review(db, user, ad):
    return Review.objects.create(text="test", author=user, ad=ad)


@pytest.mark.django_db
class TestReviewAPI:

    def test_unauthorized_user(self, api_client, review):
        list_url = reverse("reviews:review-list")
        list_response = api_client.get(list_url)
        assert list_response.status_code == status.HTTP_401_UNAUTHORIZED

        create_response = api_client.post(list_url, data={
            "text": "test_add_review_2",
            "price": 1000,
            "description": "test_description_review_2",
        })
        assert create_response.status_code == status.HTTP_401_UNAUTHORIZED

        detail_url = reverse("reviews:review-detail", kwargs={"pk": review.pk})

        put_response = api_client.put(detail_url, data={
            "title": "testput",
            "price": 1000,
            "description": "testput",
        })
        assert put_response.status_code == status.HTTP_401_UNAUTHORIZED

        patch_response = api_client.patch(detail_url, data={"title": "testpatch"})
        assert patch_response.status_code == status.HTTP_401_UNAUTHORIZED

        delete_response = api_client.delete(detail_url)
        assert delete_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authorized_user(self, api_client, user, ad, review):
        api_client.force_authenticate(user=user)

        list_url = reverse("reviews:review-list")
        list_response = api_client.get(list_url)
        assert list_response.status_code == status.HTTP_200_OK

        create_response = api_client.post(list_url, data={
            "text": "testcreate",
            "author": user.pk,
            "ad": ad.pk,
        }, format="json")
        assert create_response.status_code == status.HTTP_201_CREATED

        detail_url = reverse("reviews:review-detail", kwargs={"pk": review.pk})

        put_response = api_client.put(detail_url, data={
            "text": "testput",
            "author": user.pk,
            "ad": ad.pk,
        }, format="json")
        assert put_response.status_code == status.HTTP_200_OK

        patch_response = api_client.patch(detail_url, data={"text": "testpatch"}, format="json")
        assert patch_response.status_code == status.HTTP_200_OK

        delete_response = api_client.delete(detail_url)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT