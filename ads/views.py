from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.filters import AdvertisementFilter
from ads.models import Advertisement
from ads.pagination import AdsPagination
from ads.serializers import AdsSerializer
from permissions import IsOwnerOrAdmin


# Create your views here.

class AdsViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    pagination_class = AdsPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        if self.action in ["retrieve", "create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
