from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from djangofrontend.apps import DjangofrontendConfig
from djangofrontend.views import AdsListView, AdsDetailView, RegisterView, CustomLoginView, CustomLogoutView

app_name = DjangofrontendConfig.name

urlpatterns = [
    path("ads_list/", AdsListView.as_view(), name="ads-list"),
    path("ads_detail/<int:pk>", AdsDetailView.as_view(), name="ads-detail"),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout")

]