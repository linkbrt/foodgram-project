from django.db import models
from django.contrib.auth import get_user_model

from foodgram.models import Recipe


User = get_user_model()


class Purchase(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='purchase')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.recipe.title}'


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorite')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.recipe.title}'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
