from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class CustomUserAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email="testuser1@gmail.com",
                                                   password="testuser1",
                                                   first_name="test",
                                                   last_name="user1",
                                                   phone="88005553535")
        self.admin = CustomUser.objects.create_user(email="admin@gmail.com",
                                                   password="admin",
                                                   first_name="test",
                                                   last_name="admin",
                                                   phone="89377012108")

    def test_users_list(self):
        url = reverse("users:user-list")

        # Запрет без авторизации
        unauth_get_response = self.client.get(url)
        self.assertEqual(unauth_get_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.user)

        # Успех с авторизацией
        auth_get_response = self.client.get(url)
        self.assertEqual(auth_get_response.status_code, status.HTTP_200_OK)

        # Успешное создание юзера при авторизации
        auth_post_create_response = self.client.post(url, data={
            "email" : "test_create@mail.ru",
            "first_name" : "test",
            "last_name" : "create",
            "phone" : "88005554343",
            "password" : "testcreatepassword"
        })
        self.assertEqual(auth_post_create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(auth_post_create_response.json()["email"], "test_create@mail.ru")

    def test_users_detail(self):

        # Запрет без авторизации
        url = reverse("users:user-detail", kwargs={"pk" : self.user.pk})
        anauth_response = self.client.get(url)
        self.assertEqual(anauth_response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Успех получения юзера с авторизацией
        self.client.force_authenticate(user=self.user)
        auth_response = self.client.get(url)
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)
        self.assertEqual(auth_response.json()["email"], "testuser1@gmail.com")

        # Успешное изменение через PUT юзера по ключу
        retrieve_response = self.client.put(url, data={"email" : "testput@mail.ru",
                                                       "first_name" : "test",
                                                       "last_name" : "put",
                                                       "phone" : "88005553232",
                                                       "password" : "testput"})
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.json()["email"], "testput@mail.ru")

        # Успешное изменение через PATCH юзера по ключу
        retrieve_response = self.client.patch(url, data={"email": "testpatch@mail.ru"})
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.json()["email"], "testpatch@mail.ru")

        #Успешное удаление через DELETE юзера по ключу
        delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)


class DjosetAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email="testdjoser@gmail.com",
                                                   password="ultrahardpassword",
                                                   first_name="test",
                                                   last_name="user1",
                                                   phone="88003438383")

    def test_djoser_register(self):
        url = reverse("customuser-list")
        data = {
            "email": "testdjoser@mail.com",
            "first_name": "test",
            "last_name": "djoser",
            "phone": "88005556767",
            "password": "veryhardpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email="testdjoser@mail.com").exists())

    def test_jwt_create(self):
        create_user = data = {
            "email": "testdjoser@mail.com",
            "first_name": "test",
            "last_name": "djoser",
            "phone": "88005556767",
            "password": "veryhardpassword",
        }
        CustomUser.objects.create_user(**create_user)
        url = reverse("jwt-create")
        data = {"email" : "testdjoser@mail.com",
                "password" : "veryhardpassword"}
        response = self.client.post(url, data)
        self.assertTrue(response.json()["refresh"])
        self.assertTrue(response.json()["access"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_current_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("customuser-me")

        # Тест получения текущего пользователя
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.json()["email"], "testdjoser@gmail.com")

        # Тест изменения текущего пользователя
        patch_response = self.client.patch(url, data={"email" : "testpatch@mail.ru"})
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()["email"], "testpatch@mail.ru")

        #
