from django import forms

from .models import Recipe
from .utils import utils


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('author', 'slug', 'ingredients', 'tags')
    
    def save(self, update: bool, data: dict):
        recipe = super().save(commit=False)
        recipe.author = data['author']
        recipe.save()
        utils.set_tags_to_recipe(recipe, data.get('tags'), update)
        utils.set_ingredients_to_recipe(recipe, data.get('ingredients'), update)
        return recipe
