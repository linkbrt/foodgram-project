from django.contrib.auth import decorators
from django.db.models.aggregates import Sum
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .utils import utils

from .forms import RecipeForm
from .models import IngredientRecipe, Recipe, Tag, User

import os


def index(request: HttpRequest):
    filters = utils.get_filter_tags(request.GET.get('tags', ''))

    page, paginator = utils.paginate_request(
        filters=filters,
        list_to_paginate=Recipe.objects.all(),
        page_number=request.GET.get('page'),
    )

    response_context = {
            'page': page,
            'paginator': paginator,
            'all_tags': Tag.objects.all(),
        }

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


@decorators.login_required
def download_shopping_list(request: HttpRequest):
    result = IngredientRecipe.objects.values(
            'ingredient__title', 'ingredient__unit'
        ).annotate(
            quantity=Sum('quantity')
            )

    filename = f'shop_list_{request.user.username}.txt'
    with open(filename, 'w') as shop_file:
        for item in result:
            str_to_write = (f"{item['ingredient__title']} - " +
                            f"{item['quantity']} {item['ingredient__unit']}\n")
            shop_file.write(str_to_write)

    with open(filename, 'rb') as file:
        response = HttpResponse(file, content_type='text/txt')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        os.remove(filename)
        return response


@decorators.login_required
def user_follows(request):
    page, paginator = utils.paginate_request(
        filters=None,
        list_to_paginate=request.user.follow.select_related('author'),
        page_number=request.GET.get('page'),
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

    favorites = Recipe.objects.filter(favorite__user=request.user)
    page, paginator = utils.paginate_request(
        filters=filters,
        list_to_paginate=favorites,
        page_number=request.GET.get('page'),
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

    form = RecipeForm(
        data=request.POST or None,
        files=request.FILES or None
    )

    ingredients = request.POST.getlist('ingredients')
    error: dict = utils.validate_igredients(ingredients)
    if error:
        form.add_error('ingredients', error)


    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        recipe.tags.set(form.cleaned_data['tags'])
        utils.set_ingredients_to_recipe(recipe, ingredients)        

        return redirect(
            'single-recipe',
            username=recipe.author,
            slug=recipe.slug
        )

    return render(
        request=request,
        template_name='recipe_form.html',
        context={
            'form': form,
            'all_tags': Tag.objects.all(),
        }
    )


@decorators.login_required
def recipe_edit(request: HttpRequest, username, slug):
    recipe = get_object_or_404(Recipe, author__username=username, slug=slug)
    if request.user.username != username:
        return redirect('single-recipe', username=username, slug=slug)
    
    recipe_tags = {tag.name: 'checked' for tag in recipe.tags.all()}
    if request.method != 'POST':
        return render(
            request=request,
            template_name='recipe_form.html',
            context={
                'form': RecipeForm(instance=recipe),
                'recipe': recipe,
                'recipe_tags': recipe_tags,
                'all_tags': Tag.objects.all(),
            }
    )

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    ingredients = request.POST.getlist('ingredients')
    error: dict = utils.validate_igredients(ingredients)
    if error:
        form.add_error('ingredients', error)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.tags.set(form.cleaned_data['tags'])
        recipe.save()
        utils.set_ingredients_to_recipe(recipe, ingredients, update=True)

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
def recipe_delete(request, username, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.user.username == username:
        recipe.delete()
    return redirect('index')


def get_author_page(request, username):
    author = get_object_or_404(User, username=username)

    filters = utils.get_filter_tags(request.GET.get('tags', ''))
    page, paginator = utils.paginate_request(
        filters=filters,
        list_to_paginate=Recipe.objects.filter(author=author),
        page_number=request.GET.get('page'),
    )

    return render(
        request=request,
        template_name='user_page.html',
        context={
            'page': page,
            'paginator': paginator,
            'author': author,
            'all_tags': Tag.objects.all(),
        }
    )


def get_single_recipe_page(request, username, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.user.is_authenticated:
        purchase = request.user.purchases.filter(
            recipe=recipe
        ).exists()
    else:
        purchase = False
    return render(
        request=request,
        template_name='card_page.html',
        context={
            'recipe': recipe,
            'user_purchase': purchase,
        }
    )
