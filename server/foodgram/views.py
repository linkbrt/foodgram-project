from django.contrib.auth import decorators
from django.core.paginator import Paginator
from django.db.models.aggregates import Sum
from django.http.request import HttpRequest
from django.http.response import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

import foodgram.utils as utils

from .forms import RecipeForm
from .models import IngredientRecipe, Recipe, Tag, User


def index(request: HttpRequest):
    filters = utils.get_filter_tags(request.GET.get('tags', ''))

    page, paginator = utils.paginate_request(
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


    return render(
        request=request,
        template_name='index.html',
        context=response_context,
    )


@decorators.login_required
def shopping_list(request: HttpRequest):
    page, _ = utils.paginate_request(
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
    result = IngredientRecipe.objects.values(
            'ingredient__title'
        ).annotate(quantity=Sum('quantity')
    )

    filename = f'shop_list_{request.user.username}.txt'
    with open(filename, 'wb') as shop_file:
        for item in result:
            print(result)
            result = item['ingredient__title'] + str(item['quantity'])
            shop_file.write(bytes(result + '\n', 'utf8'))
    return FileResponse(open(filename, 'rb'))


@decorators.login_required
def user_follows(request):
    page, paginator = utils.paginate_request(
        filters=None,
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
    filters = utils.get_filter_tags(request.GET.get('tags', ''))

    raw_result = request.user.favorites.select_related('recipe')
    favorites = [purchase.recipe for purchase in raw_result]

    page, paginator = utils.paginate_request(
        filters=filters,
        list_to_paginate=favorites,
    )
    
    return render(
        request=request,
        template_name='favorite.html',
        context={
            'page': page,
            'paginator': paginator,
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

        utils.set_tags_to_recipe(recipe, data['tags'])
        utils.set_ingredients_to_recipe(recipe, data.get('ingredients'))
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

    if form.is_valid():
        recipe = form.save()
        data = dict(request.POST)
        utils.set_tags_to_recipe(recipe, data.get('tags'), update=True)
        utils.set_ingredients_to_recipe(recipe, data.get('ingredients'), update=True)
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

    filters = utils.get_filter_tags(request.GET.get('tags', ''))
    page, paginator = utils.paginate_request(
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
            'user_purchase': request.user.purchases.filter(recipe=recipe).exists(),
        }
    )
