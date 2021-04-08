from .models import Recipe
from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request=request,
        template_name='indexNotAuth.html',
        context={
            'page': page,
            'paginator': paginator,
        }
    )

def shopping_list(request):
    print(request.GET)
    print(request.user)
    pass