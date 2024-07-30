from datetime import datetime, timedelta

from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from admins.models import BranchUser, Branch
from masters.models import Timetable
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm

from admins.views import staff_required

from business_logic import BusinessLogic

logic = BusinessLogic()


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if user.is_staff:
                    return HttpResponseRedirect(reverse('admins:index'))
                return HttpResponseRedirect(reverse('masters:index'))
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()

    context = {'title': 'Авторизация',
               'form': form}
    return render(request, 'users/login.html', context)


@staff_required
def register(request, branch_id):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            branches = form.cleaned_data['branches']
            for branch in branches:
                BranchUser.objects.create(user=user, branch=branch)
            return HttpResponseRedirect(reverse('admins:all_masters', args=[branch_id]))
    else:
        form = UserRegistrationForm()
    context = {'title': ' Регистрация',
               'address': Branch.objects.get(id=branch_id),
               'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))

    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': 'Profile',
               'total_hours_in_month': logic.total_hours_in_month(request.user),
               'hours_worked_in_month': logic.hours_worked_in_month(request.user),
               'timetable_month': logic.user_timetable_month(request.user),
               'form': form}
    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))
