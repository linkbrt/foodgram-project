from django.contrib import admin
from .models import Ingredient, Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'quantity', 'measure_unit')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'tag', 'author')
    search_fields = ('title',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
