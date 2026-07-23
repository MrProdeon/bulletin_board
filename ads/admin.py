from django.contrib import admin
from ads.models import Advertisement

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_filter = ("price", )
    search_fields = ("title", "description", )
