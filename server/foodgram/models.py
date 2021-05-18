from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators

from .services import user_directory_path, pretty_slugify


User = get_user_model()


class Ingredient(models.Model):
    title = models.SlugField(max_length=150, verbose_name='Название')
    unit = models.CharField(max_length=30, verbose_name='Единица измерения')

    def __str__(self) -> str:
        return f'{self.title} - {self.unit}'


class Tag(models.Model):
    name = models.CharField(max_length=15, verbose_name='Название')
    style = models.CharField(max_length=100, verbose_name='CSS стиль')

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to=user_directory_path,
        verbose_name='Изображение'
    )
    description = models.CharField(
        max_length=300,
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name='Тэги'
    )
    cooking_time = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(1000)],
        verbose_name='Время приготовления'
    )
    slug = models.SlugField(
        unique=True,
        auto_created=True,
        verbose_name='Слаг'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время добавления'
    )

    def save(self, *args, **kwargs) -> None:
        self.slug = pretty_slugify(title=self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-pub_date']


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Игредиент'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    quantity = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(10000)
            ],
        verbose_name='Количество ингредиента'
    )

    def __str__(self) -> str:
        return f'{self.quantity}{self.ingredient.unit} \
                 {self.ingredient.title} в {self.recipe.title}'
