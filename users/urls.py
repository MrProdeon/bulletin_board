from django.urls import path
from rest_framework.urls import app_name
from rest_framework_simplejwt.views import TokenRefreshView
from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter
#from users.views import UserCreateAPIView, MyTokenObtainPairView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", MyUserViewSet, basename="user")

urlpatterns = [
    # path("register/", UserCreateAPIView.as_view(), name="register"),
    # path('login/', MyTokenObtainPairView.as_view(), name='login'),
    # path("refresh_token/", TokenRefreshView.as_view(), name="refresh-token"),


] + router.urls

