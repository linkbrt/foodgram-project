from rest_framework import serializers, validators, fields

from .models import Favorite, Follow, Purchase

class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=fields.CurrentUserDefault())
    class Meta:
        model = Purchase
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Purchase.objects.all(),
                fields=['recipe', 'user'],
            )
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=fields.CurrentUserDefault())
    
    class Meta:
        model = Favorite
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['recipe', 'user']
            )
        ]


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=fields.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author']
            )
        ]
