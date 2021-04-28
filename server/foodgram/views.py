from django.contrib.auth import decorators
from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Recipe, Tag, User
from .utils import (get_filter_tags, get_user_favorites, get_user_purchases,
                    paginate_request, set_ingredients_to_recipe,
                    set_tags_to_recipe)


def index(request: HttpRequest):
    filters = get_filter_tags(request.GET.get('tags', ''))

    page, paginator = paginate_request(
        filters=filters,
        list_to_paginate=Recipe.objects.all(),
        page_number=request.GET.get('page', '1'),
    )

    response_context = {
            'page': page,
            'paginator': paginator,
            'all_tags': Tag.objects.all(),
        }

    if not request.user.is_authenticated:
        return render(
            request=request,
            template_name='index.html',
            context=response_context,
        )
    
    response_context['purchases'] = get_user_purchases(request.user)
    response_context['favorites'] = get_user_favorites(request.user)

    return render(
        request=request,
        template_name='index.html',
        context=response_context,
    )


@decorators.login_required
def shopping_list(request: HttpRequest):
    page, _ = paginate_request(
        filters={'purchase__in': request.user.purchases.all()},
        list_to_paginate=Recipe.objects.all()
    )
    return render(
        request=request,
        template_name='shopping_list.html',
        context={
            'page': page,
        }
    )


def download_shopping_list(request: HttpRequest):
    shop_list = Recipe.objects.filter(purchase__in=request.user.purchases.all())
    result = {}
    for purchase in shop_list:
        for ingredient in purchase.ingredientrecipe_set.all():
            if result.get(ingredient.ingredient.title):
                result[ingredient.ingredient.title] += ingredient.quantity
            else:
                result[ingredient.ingredient.title] = ingredient.quantity
    filename = f'shop_list_{request.user.username}.txt'
    with open(filename, 'w') as shop_file:
        for key, value in result.items():
            print(key, value, file=shop_file)
    return FileResponse(open(filename, 'rb'))



@decorators.login_required
def user_follows(request):
    page, paginator = paginate_request(
        list_to_paginate=request.user.follow.select_related('author'),
    )
    return render(
        request=request,
        template_name='user_follows.html',
        context={
            'page': page,
            'paginator': paginator,
        }
    )


@decorators.login_required
def favorites(request):
    filters = get_filter_tags(request.GET.get('tags', ''))

    raw_result = request.user.favorites.select_related('recipe')
    favorites = [purchase.recipe for purchase in raw_result]

    page, paginator = paginate_request(
        filters=filters,
        list_to_paginate=favorites,
    )
    
    return render(
        request=request,
        template_name='favorite.html',
        context={
            'page': page,
            'paginator': paginator,
            'purchases': get_user_purchases(request.user),
            'favorites': get_user_favorites(request.user),
            'all_tags': Tag.objects.all(),
        }
    )


@decorators.login_required
def new_recipe(request: HttpRequest):
    if request.method != 'POST':
        return render(
            request=request,
            template_name='recipe_form.html',
            context={
                'form': RecipeForm(),
                'all_tags': Tag.objects.all(),
            }
        )

    form = RecipeForm(data=request.POST, files=request.FILES)
    data = dict(request.POST)
    if form.is_valid():
        recipe = form.save()
        recipe.author = request.user
        recipe.save()

        set_tags_to_recipe(recipe, data['tags'])
        set_ingredients_to_recipe(recipe, data.get('ingredients'))
        return redirect('single-recipe', username=recipe.author, slug=recipe.slug)

    return render(
        request=request,
        template_name='recipe_form.html',
        context={
            'form': form,
            'data': data,
            'form_tags': data.get('tags'),
            'all_tags': Tag.objects.all(),
        }
    )


@decorators.login_required
def recipe_edit(request: HttpRequest, username, slug):
    recipe = get_object_or_404(Recipe, author__username=username, slug=slug)
    if request.user.username != username:
        return redirect('single-recipe', username=username, slug=slug)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    
    recipe_tags = {tag.name: 'checked' for tag in recipe.tags.all()}

    if request.method == 'POST' and form.is_valid():
        recipe = form.save()
        data = dict(request.POST)
        set_tags_to_recipe(recipe, data.get('tags'), update=True)
        set_ingredients_to_recipe(recipe, data.get('ingredients'), update=True)
        return redirect('single-recipe', username=username, slug=recipe.slug)

    return render(
            request=request,
            template_name='recipe_form.html',
            context={
                'form': form,
                'recipe': recipe,
                'recipe_tags': recipe_tags,
                'all_tags': Tag.objects.all(),
            }
    )

@decorators.login_required
def get_requested_user_page(request, username):
    user = get_object_or_404(User, username=username)

    filters = get_filter_tags(request.GET.get('tags', ''))
    page, paginator = paginate_request(
        filters=filters,
        list_to_paginate=Recipe.objects.filter(author=user),
    )

    return render(
        request=request,
        template_name='user_page.html',
        context={
            'page': page,
            'paginator': paginator,
            'user': user,
            'user_follow': request.user.follow.filter(author=user).exists(),
            'purchases': get_user_purchases(request.user),
            'favorites': get_user_favorites(request.user),
            'all_tags': Tag.objects.all(),
        }
    )

@decorators.login_required
def get_single_recipe_page(request, username, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(
        request=request,
        template_name='card_page.html',
        context={
            'recipe': recipe,
            'user_follow': request.user.follow.filter(author=recipe.author).exists(),
            'user_purchase': request.user.purchases.filter(recipe=recipe).exists(),
        }
    )
