from django.contrib import admin
from django.contrib.auth import get_user_model


profile = get_user_model()


@admin.register(profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
