from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from reviews.models import Review
from reviews.serializers import ReviewSerializer


# Create your views here.

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
