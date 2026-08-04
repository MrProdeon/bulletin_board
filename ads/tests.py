from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ads.models import Advertisement
from users.models import CustomUser

class AdvertisementAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email="testadduser@gmail.com",
                                                   password="testaddduser",
                                                   first_name="test",
                                                   last_name="adduser",
                                                   phone="88003837363")

        self.second_user = CustomUser.objects.create_user(email="secondtestadduser@gmail.com",
                                                   password="secondtestaddduser",
                                                   first_name="secondtest",
                                                   last_name="adduser",
                                                   phone="88002783726")

        self.add = Advertisement.objects.create(title="test_add",
                                                price=100,
                                                description="test_description",
                                                author=self.user)

        self.second_add = Advertisement.objects.create(title="test_add2",
                                                price=1002,
                                                description="test_description2",
                                                author=self.second_user)

    def test_current_user_ads(self):
        """Тесты с объявлениями текущего пользователя"""

        # Тест просмотра чужого объявления без авторизации
        url_retrieve = reverse("ads:ad-detail", kwargs={"pk" : self.add.pk})
        retrieve_response = self.client.get(url_retrieve)
        self.assertEqual(retrieve_response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Тест получения списка объявлений
        url_list = reverse("ads:ad-list")
        self.client.force_authenticate(user=self.user)
        response_list = self.client.get(url_list)
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list.json()["results"]), 2)

        # Тест создания нового объявления
        url_create = reverse("ads:ad-list")
        response_create = self.client.post(url_create, data={
            "title": "testcreate",
            "price": 500,
            "description": "test_create",
            "author": self.user
        })
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Advertisement.objects.filter(title="testcreate").exists())


        url_detail = reverse("ads:ad-detail", kwargs={"pk": self.add.pk})

        # Тест получения одного объявления
        response_detail = self.client.get(url_detail)

        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.json()["title"], "test_add")

        # Тест изменения объявления
        response_patch = self.client.patch(url_detail, data={"title" : "testpatch"})
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertTrue(Advertisement.objects.filter(title="testpatch").exists())

        # Тест удаления объявления
        response_delete = self.client.delete(url_detail)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_user_ads(self):

        #Тест попытки обновить/удалить чужое объявление
        url_update = reverse("ads:ad-detail", kwargs={"pk" : self.second_add.pk})
        patch_response = self.client.patch(url_update, data={"title" : "test_patch"})
        self.assertEqual(patch_response.status_code, status.HTTP_401_UNAUTHORIZED)

        put_response = self.client.put(url_update, data={
            "title" : "test_put",
            "price" : 500,
            "description" : "testput"
        })
        self.assertEqual(put_response.status_code, status.HTTP_401_UNAUTHORIZED)

        delete_response = self.client.delete(url_update)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)











