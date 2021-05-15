from django.db import models
from django.contrib.auth import get_user_model

from foodgram.models import Recipe


User = get_user_model()


class Purchase(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='purchase',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='В покупках'
    )

    def __str__(self) -> str:
        return f'{self.user.username} - {self.recipe.title}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique purchase')
        ]


class Favorite(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='В избранном'
    )

    def __str__(self) -> str:
        return f'{self.user.username} - {self.recipe.title}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique favorite')
        ]


class Follow(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='follow',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Автор'
    )

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow')
        ]
