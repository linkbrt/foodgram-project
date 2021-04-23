from django import forms
from django.db.models import fields
from django.core import validators

from .models import Recipe


class RecipeForm(forms.ModelForm):
    # title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    # description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form__textarea'}))

    class Meta:
        model = Recipe
        exclude = ('author', 'slug', 'ingredients', 'tags')
    
