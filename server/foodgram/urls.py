from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('shopping-list/', views.shopping_list, name='shopping-list')
]