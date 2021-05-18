from django.contrib.auth import (authenticate, decorators, forms, login,
                                 logout, update_session_auth_hash)
from django.http import request, response
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomUserCreationForm
from .models import Profile


def login_view(request: request.HttpRequest):
    form = forms.AuthenticationForm()
    if request.method != 'POST':
        return render(
                request=request,
                template_name='user-login.html',
                context={
                    'form': form,
                }
            )

    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )
    if not user:
        return render(
            request=request,
            template_name='user-login.html',
            context={
                'login_error': 'Имя пользователя и пароль не совпадают. \
                                Введите правильные данные.',
                'form': form,
            }
        )
    if user.is_active:
        login(request, user)
        return redirect(to='index')

    return response.HttpResponse({'error': 'Аккаунт заблокирован'})


def logout_view(request: request.HttpRequest):
    logout(request)
    return redirect(to='index')


@decorators.login_required
def change_password(request: request.HttpRequest):
    if request.method != 'POST':
        form = forms.PasswordChangeForm(request.user)
        return render(request, 'password-change.html', {'form': form})

    form = forms.PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('index')

    return render(request, 'password-change.html', {'form': form})


def registration_user(request: request.HttpRequest):
    if request.method != 'POST':
        form = CustomUserCreationForm()
        return render(request, 'user-registration.html', {'form': form})

    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        new_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        login(request, new_user)
        return redirect('index')
    return render(request, 'user-registration.html', {'form': form})
