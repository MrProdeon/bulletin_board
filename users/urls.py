from django.urls import path
from rest_framework.urls import app_name
from users.apps import UsersConfig
from users.views import UserCreateAPIView, MyTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

]
