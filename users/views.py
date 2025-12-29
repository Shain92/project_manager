from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm


def login_view(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('users:home')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('users:home')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('users:login')


def register_view(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('users:home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Регистрация успешна! Добро пожаловать, {user.username}!')
            return redirect('users:home')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def home_view(request):
    """Главная страница"""
    return render(request, 'users/home.html')

