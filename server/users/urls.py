from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', views.change_password, name='password-change'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
            template_name='password-reset.html',
         ),
         name='password-reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password-reset-done.html',
         ),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password-reset-confirm.html',
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password-reset-complete.html',
         ),
         name='password_reset_complete'),
    path('registration/', views.registration_user, name='registration'),
]
