from typing import Any, Optional

from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from ..models import Ingredient, IngredientRecipe, Recipe, Tag


def get_filter_tags(filter_tags: Any):
    if not filter_tags:
        return {}

    filter_tags = filter_tags.split(',')
    return {'tags__in': [get_object_or_404(Tag, name=tag) for tag in filter_tags]}


def paginate_request(filters: Optional[dict], list_to_paginate: QuerySet, page_number: str = '1'):
    if filters is not None:
        list_to_paginate = list_to_paginate.filter(**filters).distinct()

    paginator = Paginator(list_to_paginate, 6)
    page = paginator.get_page(page_number)
    return page, paginator


def validate_igredients(data: list):
    errors = []
    if not data:
        return 'Обязательное поле'
    
    for item in data:
        title = item.split('-')[0]
        ingredient = Ingredient.objects.filter(title=title)

        if not ingredient.exists():
            errors.append(f'{item} неверное значение')

    return ', '.join(errors)


def ingredients_to_python(data: list) -> list:
    result = []
    for item in data:
        title, quantity = item.split('-')
        ingredient = Ingredient.objects.get(title=title)
        result.append({'ingredient': ingredient, 'quantity': int(quantity)})
    return result


def set_ingredients_to_recipe(instance: Recipe, ingredients: list, **kwargs) -> None:
    ingredients: list = ingredients_to_python(ingredients)
    if kwargs.get('update'):
        IngredientRecipe.objects.filter(recipe=instance).delete()
    create_query = []

    for item in ingredients:
        create_query.append(
            IngredientRecipe(
                recipe=instance,
                ingredient=item['ingredient'],
                quantity=item['quantity'],
            )
        )
    IngredientRecipe.objects.bulk_create(create_query)
