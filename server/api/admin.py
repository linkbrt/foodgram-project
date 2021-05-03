from django.contrib import admin

from .models import Purchase, Favorite, Follow


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass
