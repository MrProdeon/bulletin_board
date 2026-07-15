from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from ads.filters import AdvertisementFilter
from ads.models import Advertisement
from ads.pagination import AdsPagination
from ads.serializers import AdsSerializer


# Create your views here.

class AdsViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    pagination_class = AdsPagination


