from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from .models import Ingredient, IngredientRecipe, Recipe, Tag, User
from .forms import RecipeForm
from .recipe_logic.utils import set_ingredients_to_recipe, set_tags_to_recipe


def index(request: HttpRequest):
    if not request.user.is_authenticated:
        return render(
            request=request,
            template_name='foodgram/index.html'
        )
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    purchases_list = request.user.purchases.select_related('recipe')
    result = [purchase.recipe for purchase in purchases_list]
    return render(
        request=request,
        template_name='foodgram/index.html',
        context={
            'page': page,
            'paginator': paginator,
            'purchases': result,
        }
    )

def shopping_list(request: HttpRequest):
    result = Recipe.objects.filter(purchase__in=request.user.purchases.all())
    return render(
        request=request,
        template_name='foodgram/shopping_list.html',
        context={
            'result': result,
        }
    )

def user_follows(request):
    result = request.user.follow.select_related('author')
    paginator = Paginator(result, 3)
    page = paginator.get_page(request.GET.get('page'))
    return render(
        request=request,
        template_name='foodgram/user_follows.html',
        context={
            'page': page,
            'paginator': paginator,
        }
    )

def favorites(request):
    favorites_list = request.user.favorites.select_related('recipe')
    result = [favorite.recipe for favorite in favorites_list]
    paginator = Paginator(result, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    purchases_list = request.user.purchases.select_related('recipe')
    result = [purchase.recipe for purchase in purchases_list]
    return render(
        request=request,
        template_name='foodgram/favorite.html',
        context={
            'page': page,
            'paginator': paginator,
            'purchases': result,
        }
    )

def new_recipe(request: HttpRequest):
    form = RecipeForm()
    if request.method == 'POST':
        form = RecipeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            data = dict(request.POST)
            set_tags_to_recipe(recipe, data['tags'])
            set_ingredients_to_recipe(recipe, data.get('ingredients'))
        print(form.data)
    return render(
        request=request,
        template_name='foodgram/recipe_create.html',
        context={
            'form': form,
        }
    )


def recipe_edit(request: HttpRequest, username, slug):
    recipe = get_object_or_404(Recipe, author__username=username, slug=slug)
    if request.user.username != username:
        return redirect('single-recipe', username=username, slug=slug)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        recipe = form.save()
        data = dict(request.POST)
        set_tags_to_recipe(recipe, data.get('tags'), update=True)
        set_ingredients_to_recipe(recipe, data.get('ingredients'), update=True)
        return redirect('single-recipe', username=username, slug=recipe.slug)
    # print(form.errors)
    # print(form.fields)
    tags_to_render = {}
    for tag in recipe.tags.all():
        tags_to_render[tag.name] = 'checked'
    return render(request, 'foodgram/recipe_change.html', {
        'form': form,
        'recipe': recipe,
        'tags': tags_to_render,
    })

def get_requested_user_page(request, username):
    user = get_object_or_404(User, username=username)
    user_recipes_list = Recipe.objects.filter(author=user)
    paginator = Paginator(user_recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request=request,
        template_name='foodgram/authorRecipe.html',
        context={
            'page': page,
            'paginator': paginator,
            'user': user,
        }
    )

def get_single_recipe_page(request, username, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    user_follows = [follow.author for follow in request.user.follow.all()]
    return render(
        request=request,
        template_name='foodgram/singlePage.html',
        context={
            'recipe': recipe,
            'user_follows': user_follows,
        }
    )

def user_directory_path(instance, filename):
    return f'recipies/{instance.author.username}/{filename}'
