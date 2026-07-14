from django.urls import path
from rest_framework.urls import app_name
from rest_framework_simplejwt.views import TokenRefreshView
from users.apps import UsersConfig
#from users.views import UserCreateAPIView, MyTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    # path("register/", UserCreateAPIView.as_view(), name="register"),
    # path('login/', MyTokenObtainPairView.as_view(), name='login'),
    # path("refresh_token/", TokenRefreshView.as_view(), name="refresh-token"),

]
