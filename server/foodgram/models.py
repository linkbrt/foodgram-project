from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators

from .services import user_directory_path, pretty_slugify


User = get_user_model()


class Ingredient(models.Model):
    title = models.SlugField(max_length=30)
    unit = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f'{self.title} - {self.unit}'


class Tag(models.Model):
    name = models.CharField(max_length=15)
    style = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.CharField(max_length=300)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe')
    tags = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(1000)])
    slug = models.SlugField(unique=True, auto_created=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs) -> None:
        self.slug = pretty_slugify(title=self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-pub_date']


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.SET_NULL, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(10000)])
