from rest_framework.serializers import ModelSerializer
from ads.models import Advertisement

class AdsSerializer(ModelSerializer):
    class Meta:
        model = Advertisement
        fields = "__all__"
        read_only_fields = ["author"]