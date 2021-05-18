from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(max_length=100, required=False)
    class Meta:
        model = Recipe
        exclude = ('author', 'slug')
    
    widgets = {
        'tags': forms.CheckboxSelectMultiple(),
    }
