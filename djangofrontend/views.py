from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView
from rest_framework.reverse import reverse_lazy

from ads.models import Advertisement
from django.views import View
from djangofrontend.forms import CustomUserCreationForm

class AdsListView(ListView):
    model = Advertisement
    template_name = "ads/ads_list.html"
    context_object_name = "ads"

class AdsDetailView(DetailView):
    model = Advertisement
    template_name = "ads/ads_detail.html"
    context_object_name = "ad"

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("djangofrontend:ads-list")

class CustomLoginView(LoginView):
    template_name = "users/login.html"

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("djangofrontend:ads-list")