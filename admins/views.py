from datetime import datetime, timedelta

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from masters.models import Timetable
from users.forms import UserProfileForm
from .models import Branch, User


def index(request):
    context = {
        'title': 'admins',
        'branches': Branch.objects.filter(branchuser__user=request.user)
    }
    return render(request, 'admins/index.html', context)


def all_masters(request, branch_id):
    context = {
        'title': 'all_masters',
        'branches': Branch.objects.filter(branchuser__user=request.user),
        'address': Branch.objects.get(id=branch_id),
        'masters': User.objects.filter(branchuser__branch_id=branch_id)
    }
    return render(request, 'admins/all_masters.html', context)


def master(request, master_id, branch_id):
    user = User.objects.get(id=master_id)
    if request.method == 'POST':
        form = UserProfileForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:master'))

    else:
        form = UserProfileForm(instance=user)
    context = {'title': 'Profile',
               'total_hours_in_month': total_hours_in_month(user),
               'hours_worked_in_month': hours_worked_in_month(user),
               'timetable_month': user_timetable_month(user),
               'branches': Branch.objects.filter(branchuser__user=request.user),
               'address': Branch.objects.get(id=branch_id),
               'masters': User.objects.filter(branchuser__branch_id=branch_id),
               'form': form}
    return render(request, 'admins/master_profile.html', context)

def schedule(request, branch_id, date):
    if request.method == 'POST':
        action = request.POST['action']
        chair_num = request.POST.get('chair_num')
        shift_mon = request.POST.get('shift_mon')
        shift_eve = request.POST.get('shift_eve')
        user_id = request.POST.get('last_name')
        if action == 'add':
            if shift_mon == 'Yes' and shift_eve == 'No':
                add_or_update_timetable_shift_mon(
                    branch=int(branch_id),
                    user=user_id,
                    chair_num=chair_num,
                    date=date)
            elif shift_mon == 'No' and shift_eve == 'Yes':
                add_or_update_timetable_shift_eve(
                    branch=int(branch_id),
                    user=user_id,
                    chair_num=chair_num,
                    date=date)
        elif action == 'del':
            if shift_mon == 'Yes' and shift_eve == 'No':
                delete_timetable_mon(
                    branch=int(branch_id),
                    user=user_id,
                    chair_num=chair_num,
                    date=date)
            elif shift_mon == 'No' and shift_eve == 'Yes':
                delete_timetable_eve(
                    branch=int(branch_id),
                    user=user_id,
                    chair_num=chair_num,
                    date=date)

    quantity_chairs = Branch.objects.get(id=branch_id).chairs
    context = {
        'title': 'Расписание',
        'branches': Branch.objects.filter(branchuser__user=request.user),
        'chairs': quantity_chairs,
        'address': Branch.objects.get(id=branch_id),
        'branch_id': Branch.objects.get(id=branch_id).id,
        'date': date,
        'format_date': format_date(date),
        'timetables_data': get_timetables_data(branch_id, date),
        'masters': User.objects.filter(branchuser__branch_id=branch_id)
    }

    return render(request, 'admins/schedule_admin.html', context)


def get_timetables_data(branch_id, date):
    timetables_list = []
    data_timetables = Timetable.objects.filter(branch=branch_id, date=date).all()
    quantity_chairs = Branch.objects.get(id=branch_id).chairs
    for chair in range(1, quantity_chairs + 1):
        timetables = {}
        timetable_mon = data_timetables.filter(chair_number=chair, shift_mon=True).first()
        timetable_eve = data_timetables.filter(chair_number=chair, shift_eve=True).first()
        timetables['num'] = chair
        timetables['t_mon_dict'] = ''
        timetables['t_eve_dict'] = ''
        if timetable_mon:
            timetables['t_mon_dict'] = {'first_name': timetable_mon.user.first_name,
                                        'last_name': timetable_mon.user.last_name,
                                        'image': timetable_mon.user.image,
                                        'id': timetable_mon.user.id}
        if timetable_eve:
            timetables['t_eve_dict'] = {'first_name': timetable_eve.user.first_name,
                                        'last_name': timetable_eve.user.last_name,
                                        'image': timetable_eve.user.image,
                                        'id': timetable_eve.user.id}
        timetables_list.append(timetables)
    return timetables_list


def format_date(date):
    date = datetime.strptime(date, '%Y-%m-%d')

    months = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]

    formatted_date = f"{date.day} {months[date.month - 1]} {date.year}"

    return formatted_date


def add_or_update_timetable_shift_mon(branch, user, chair_num, date):
    with transaction.atomic():
        branch = Branch.objects.get(id=branch)
        user = User.objects.get(id=user)
        timetable, created = Timetable.objects.get_or_create(
            branch=branch,
            user=user,
            chair_number=chair_num,
            date=date,
            defaults={'shift_mon': True, 'shift_eve': False}
        )
        if not created:
            timetable.shift_mon = True
            timetable.save()


def add_or_update_timetable_shift_eve(branch, user, chair_num, date):
    branch = Branch.objects.get(id=branch)
    user = User.objects.get(id=user)
    with transaction.atomic():
        timetable, created = Timetable.objects.get_or_create(
            branch=branch,
            user=user,
            chair_number=chair_num,
            date=date,
            defaults={'shift_mon': False, 'shift_eve': True}
        )
        if not created:
            timetable.shift_eve = True
            timetable.save()


def delete_timetable_mon(branch, user, chair_num, date):
    branch = Branch.objects.get(id=branch)
    user = User.objects.get(id=user)
    with transaction.atomic():
        try:
            timetable = Timetable.objects.get(
                branch=branch,
                user=user,
                chair_number=chair_num,
                date=date
            )
            if timetable.shift_mon and timetable.shift_eve:
                timetable.shift_mon = False
                timetable.save()
            else:
                timetable.delete()
            print("Запись успешно удалена.")
        except Timetable.DoesNotExist:
            print("Запись не найдена.")


def delete_timetable_eve(branch, user, chair_num, date):
    branch = Branch.objects.get(id=branch)
    user = User.objects.get(id=user)
    with transaction.atomic():
        try:
            timetable = Timetable.objects.get(
                branch=branch,
                user=user,
                chair_number=chair_num,
                date=date
            )
            if timetable.shift_mon and timetable.shift_eve:
                timetable.shift_eve = False
                timetable.save()
            else:
                timetable.delete()
            print("Запись успешно удалена.")
        except Timetable.DoesNotExist:
            print("Запись не найдена.")

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
    timetable_month = []
    current_date = datetime.now()
    first_day_of_month = current_date.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    timetable_records = Timetable.objects.filter(
        Q(user=user) &
        Q(date__gte=first_day_of_month) &
        Q(date__lte=last_day_of_month)
    )

    for timetable_record in timetable_records:
        timetable_day = {}
        timetable_day['date'] = timetable_record.date.strftime("%d.%m.%Y")
        timetable_day['branch'] = timetable_record.branch.address
        timetable_day['chair_number'] = timetable_record.chair_number
        if timetable_record.shift_mon and timetable_record.shift_eve:
            timetable_day['start_time'] = '9:00'
            timetable_day['end_time'] = '20:00'
        elif timetable_record.shift_mon:
            timetable_day['start_time'] = '9:00'
            timetable_day['end_time'] = '15:00'
        elif timetable_record.shift_eve:
            timetable_day['start_time'] = '15:00'
            timetable_day['end_time'] = '20:00'
        timetable_month.append(timetable_day)
    return timetable_month
