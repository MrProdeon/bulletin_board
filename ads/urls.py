from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ads.apps import AdsConfig
from ads.views import AdsViewSet

app_name = AdsConfig.name

router = DefaultRouter()
router.register(r"", AdsViewSet, basename="ad")

urlpatterns = [] + router.urls