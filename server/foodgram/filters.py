import django_filters

from .models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.MultipleChoiceFilter(
        field_name='tags',
        lookup_expr='icontains'
    )

    class Meta:
        model = Recipe
        fields = ['tags']
