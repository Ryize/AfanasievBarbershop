from datetime import datetime, timedelta

from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from admins.models import BranchUser, Branch
from masters.models import Timetable
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


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
            print(form.errors)
    else:
        form = UserLoginForm()

    context = {'title': 'Авторизация',
               'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            branches = form.cleaned_data['branches']
            for branch in branches:
                BranchUser.objects.create(user=user, branch=branch)
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'title': ' Регистрация',
               'form': form}
    return render(request, 'users/register.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))

    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': 'Profile',
               'total_hours_in_month': total_hours_in_month(request.user),
               'hours_worked_in_month': hours_worked_in_month(request.user),
               'user_timetable_month': user_timetable_month(request.user),
               'form': form}
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))

def total_hours_in_month(user):
    current_date = datetime.now()
    total_hours_in_month = 0

    first_day_of_month = current_date.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    timetable_records = Timetable.objects.filter(
        Q(user=user) &
        Q(date__gte=first_day_of_month) &
        Q(date__lte=last_day_of_month)
    )
    for _ in timetable_records:
        if _.shift_mon:
            total_hours_in_month += 8
        if _.shift_eve:
            total_hours_in_month += 5
    return total_hours_in_month


def hours_worked_in_month(user):
    current_date = datetime.now()
    hours_worked_in_month = 0

    first_day_of_month = current_date.replace(day=1)

    timetable_records = Timetable.objects.filter(
        Q(user=user) &
        Q(date__gte=first_day_of_month) &
        Q(date__lte=current_date - timedelta(days=1))
    )
    for _ in timetable_records:
        if _.shift_mon:
            hours_worked_in_month += 8
        if _.shift_eve:
            hours_worked_in_month += 5
    return hours_worked_in_month


def user_timetable_month(user):
    current_date = datetime.now()
    first_day_of_month = current_date.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)


    timetable_records = Timetable.objects.filter(
        Q(user=user) &
        Q(date__gte=first_day_of_month) &
        Q(date__lte=last_day_of_month)
    )

    return timetable_records
