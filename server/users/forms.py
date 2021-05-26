from django.contrib.auth import forms
from .models import Profile
from typing import Any


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm):
        model = Profile
        fields = ('first_name', 'username', 'email')
