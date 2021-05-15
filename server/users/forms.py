from django.contrib.auth import forms
from .models import Profile
from typing import Any


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm):
        model = Profile
        fields = ('email', 'username')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class CustomAuthenticationForm(forms.AuthenticationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class CustomPasswordResetForm(forms.PasswordResetForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'
