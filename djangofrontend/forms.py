from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import CustomUser

# Форма регистрации
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["email", "first_name", "last_name", "phone"]

# Форма авторизации
class CustomAuthenticationForm(AuthenticationForm):
    pass