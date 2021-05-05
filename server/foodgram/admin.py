from django.contrib import admin
from .models import Ingredient, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'unit')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    pass


class IngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author')
    search_fields = ('title',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('title',)}
    inlines = (IngredientInLine,)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
