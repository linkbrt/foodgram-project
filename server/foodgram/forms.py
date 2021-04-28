from django import forms
from django.db.models import fields
from django.core import validators

from .models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('author', 'slug', 'ingredients', 'tags')
    
