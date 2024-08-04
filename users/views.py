"""
Модуль содержит функции представления для управления пользователями: вход, регистрация, профиль и выход.
"""

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from admins.views import staff_required
from services.business_logic import BusinessLogic
from services.data_access import DataAccess
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

# Инициализация бизнес-логики и доступа к данным.
logic = BusinessLogic()
dataAccess = DataAccess()


def login(request):
    """
    Обработчик для страницы входа в систему.

    Args:
        request: Запрос HTTP.

    Returns:
        HttpResponse: HTML-код страницы входа в систему.
    """
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if user:
                auth.login(request, user)
                if user.is_staff:
                    return HttpResponseRedirect(reverse('admins:index'))
                return HttpResponseRedirect(reverse('masters:index'))
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()

    context = {'title': 'Авторизация', 'form': form}
    return render(request, 'users/login.html', context)


@staff_required
def register(request, branch_id: int):
    """
    Обработчик для страницы регистрации нового пользователя.

    Args:
        request: Запрос HTTP.
        branch_id (int): Идентификатор филиала.

    Returns:
        HttpResponse: HTML-код страницы регистрации.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            branches = form.cleaned_data['branches']
            dataAccess.add_branch_user(user, branches)
            return HttpResponseRedirect(reverse('admins:all_masters', args=[branch_id]))
    else:
        form = UserRegistrationForm()
    context = {'title': 'Регистрация', 'address': dataAccess.get_branch(branch_id), 'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    """
    Обработчик для страницы профиля пользователя.

    Args:
        request: Запрос HTTP.

    Returns:
        HttpResponse: HTML-код страницы профиля пользователя.
    """
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'Profile',
        'total_hours_in_month': logic.total_hours_in_month(request.user),
        'hours_worked_in_month': logic.hours_worked_in_month(request.user),
        'timetable_month': logic.user_timetable_month(request.user),
        'form': form
    }
    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    """
    Обработчик для выхода из системы.

    Args:
        request: Запрос HTTP.

    Returns:
        HttpResponseRedirect: Перенаправление на страницу входа в систему.
    """
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))
