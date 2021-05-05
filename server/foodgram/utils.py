from typing import Any, Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from .models import Ingredient, IngredientRecipe, Recipe, Tag


def get_filter_tags(filter_tags: Any):
    if not filter_tags:
        return {}

    filter_tags = filter_tags.split(',')
    return {'tags__in': [get_object_or_404(Tag, name=tag) for tag in filter_tags]}


def paginate_request(filters: Optional[dict], list_to_paginate: QuerySet, page_number: str='1'):
    if filters is not None:
        list_to_paginate = list_to_paginate.filter(**filters)

    paginator = Paginator(list_to_paginate, 6)
    page = paginator.get_page(page_number)
    return page, paginator


def set_tags_to_recipe(instance: Recipe, tags, update: bool=False):
    if update:
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
        ingredient = get_object_or_404(Ingredient, title=title)
        create_query.append(
            IngredientRecipe(
                recipe=instance,
                ingredient=ingredient,
                quantity=int(value)
            )
        )
    IngredientRecipe.objects.bulk_create(create_query)
