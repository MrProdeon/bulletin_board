from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from ads.models import Advertisement
from ads.serializers import AdsSerializer


# Create your views here.

class AdsViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdsSerializer
