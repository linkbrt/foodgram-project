from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UnitChoises(models.TextChoices):
    GRAMS = 'г'
    MILLILITRES = 'мл'
    TABLES_SPOON = 'ст.л'
    PINCH = 'щепотка'
    TO_TASTE = 'по вкусу'
    ITEM = 'шт'


class Ingredient(models.Model):
    title = models.SlugField(max_length=30)
    quantity = models.IntegerField()
    measure_unit = models.CharField(choices=UnitChoises.choices, max_length=10)


class TagChoises(models.Choices):
    BREAKFAST = 'Завтрак'
    LUNCH = 'Обед'
    DINNER = 'Ужин'


def user_directory_path(instance, filename):
    return f'recipies/{instance.author.username}/{filename}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.CharField(max_length=300)
    ingredients = models.ManyToManyField(Ingredient)
    tag = models.CharField(choices=TagChoises.choices, default=TagChoises.LUNCH, max_length=7)
    cooking_time = models.IntegerField(validators=[])
    slug = models.SlugField()
