from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('shopping-list/', views.shopping_list, name='shopping-list'),
    path('shopping-list/download/', views.download_shopping_list, name='download'),
    path('follows/', views.user_follows, name='user-follows'),
    path('favorites/', views.favorites, name='favorites'),
    path('new/', views.new_recipe, name='new-recipe'),
    
    path('<str:username>/', views.get_requested_user_page, name='user-page'),
    path('<str:username>/<slug:slug>/', views.get_single_recipe_page, name='single-recipe'),
    path('<str:username>/<slug:slug>/edit/', views.recipe_edit, name='recipe-edit'),
]