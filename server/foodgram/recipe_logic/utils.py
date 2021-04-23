from typing import Any, List

from ..models import Ingredient, IngredientRecipe, Recipe, Tag


def set_tags_to_recipe(instance: Recipe, tags, update: bool=False):
    if update:
        # print(instance.title)
        instance.tags.clear()
    for tag in tags:
        instance.tags.add(Tag.objects.get(name=tag))


def set_ingredients_to_recipe(instance: Recipe, ingredients, update: bool=False):
    if update:
        IngredientRecipe.objects.filter(recipe=instance).delete()
    create_query = []
    if not ingredients:
        return
    for item in ingredients:
        title, value = item.split('-')
        create_query.append(
            IngredientRecipe(
                recipe=instance,
                ingredient=Ingredient.objects.get(title=title),
                quantity=int(value)
            )
        )
    IngredientRecipe.objects.bulk_create(create_query)
