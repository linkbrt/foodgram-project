from django.contrib.auth import forms
from .models import Profile
from typing import Any


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm):
        model = Profile
        fields = ('email', 'username', 'first_name')
