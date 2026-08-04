from rest_framework.test import APITestCase
from reviews.models import Review
from users.models import CustomUser
from ads.models import Advertisement
from django.urls import reverse
from rest_framework import status


class ReviewAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email="testuserreview@gmail.com",
                                                   password="testuserreview",
                                                   first_name="testreview",
                                                   last_name="user1",
                                                   phone="88005559835")
        self.add = Advertisement.objects.create(title="test_add_review",
                                                price=1000,
                                                description="test_description_review",
                                                author=self.user)
        self.review = Review.objects.create(text="test",
                                            author=self.user,
                                            ad=self.add)

    def test_unauthorized_user(self):
        list_url = reverse("reviews:review-list")
        list_response = self.client.get(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_401_UNAUTHORIZED)
        create_response = self.client.post(list_url, data={"text": "test_add_review_2", "price": 1000,
                                                           "description": "test_description_review_2"})
        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)

        detail_url = reverse("reviews:review-detail", kwargs={"pk" : self.review.pk})
        put_response = self.client.put(detail_url,data={"title": "testput", "price": 1000,
                                                           "description": "testput"})
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)

        patch_response = self.client.patch(detail_url, data={"title": "testpatch"})
        self.assertEqual(patch_response.status_code, status.HTTP_401_UNAUTHORIZED)

        delet_response = self.client.delete(detail_url)
        self.assertEqual(delet_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_user(self):
        self.client.force_authenticate(user=self.user)
        list_url = reverse("reviews:review-list")
        list_response = self.client.get(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        create_response = self.client.post(list_url, data={
            "text": "testcreate",
            "author": self.user.pk,
            "ad": self.add.pk,
        }, format="json")
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        detail_url = reverse("reviews:review-detail", kwargs={"pk": self.review.pk})
        put_response = self.client.put(detail_url, data={
            "text": "testput",
            "author": self.user.pk,
            "ad": self.add.pk,
        }, format="json")
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        patch_response = self.client.patch(detail_url, data={"text": "testpatch"}, format="json")
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        delet_response = self.client.delete(detail_url)
        self.assertEqual(delet_response.status_code, status.HTTP_204_NO_CONTENT)