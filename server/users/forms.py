from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Profile
        fields = ("username",)
