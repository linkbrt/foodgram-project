from api.models import Purchase, Favorite
from django import template
from django.utils.http import urlencode

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def word_declination(word, count):
    if count == 1:
        return 'рецепт'
    elif count  < 5:
        return 'рецепта'
    return 'рецептов'


@register.filter
def in_purchases(recipe, user) -> bool:
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def in_favorites(recipe, user) -> bool:
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag(takes_context=True)
def url_params_replace(context, **kwargs):
    query: dict = context['request'].GET.dict()
    tags = query.get('tags')
    if tags:
        tags = list(tags.split(','))
    else:
        tags = []
    tag = kwargs['tag']
    del kwargs['tag']
    if tag in tags:
        tags.remove(tag)
    else:
        tags.append(tag)
    query.update(kwargs, tags=','.join(tags))
    return urlencode(query)
