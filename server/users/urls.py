from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', views.change_password, name='password-change'),
    path('password-reset/', views.password_reset, name='password-reset'),
    path('registration/', views.registration_user, name='registration'),
]