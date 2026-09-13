import django_filters
from ads.models import Advertisement

class AdvertisementFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Advertisement
        fields = ["title"]