from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction

from .models import Timetable, Branch


def index(request):
    context = {
        'title': 'masters',
        'branches': Branch.objects.all(),
    }
    return render(request, 'index.html', context)


def schedule(request, branch_id, date):
    if request.method == 'POST':
        action = request.POST['action']
        chair_num = request.POST.get('chair_num')
        shift_mon = request.POST.get('shift_mon')
        shift_eve = request.POST.get('shift_eve')
        if action == 'add':
            if shift_mon == 'Yes' and shift_eve == 'No':
                add_or_update_timetable_shift_mon(
                    branch=int(branch_id),
                    user=request.user,
                    chair_num=chair_num,
                    date=date)
            elif shift_mon == 'No' and shift_eve == 'Yes':
                add_or_update_timetable_shift_eve(
                    branch=int(branch_id),
                    user=request.user,
                    chair_num=chair_num,
                    date=date)
        elif action == 'del':
            if shift_mon == 'Yes' and shift_eve == 'No':
                delete_timetable_mon(
                    branch=int(branch_id),
                    user=request.user,
                    chair_num=chair_num,
                    date=date)
            elif shift_mon == 'No' and shift_eve == 'Yes':
                delete_timetable_eve(
                    branch=int(branch_id),
                    user=request.user,
                    chair_num=chair_num,
                    date=date)

        print(chair_num, shift_mon, shift_eve, action, request.user.id, branch_id, date)

    quantity_chairs = Branch.objects.get(id=branch_id).chairs
    context = {
        'title': 'Расписание',
        'branches': Branch.objects.all(),
        'chairs': quantity_chairs,
        'address': Branch.objects.get(id=branch_id).address,
        'branch_id': Branch.objects.get(id=branch_id).id,
        'date': date,
        'format_date': format_date(date),
        'timetables_data': get_timetables_data(branch_id, date),
    }

    return render(request, 'schedule.html', context)


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
        # print(timetable_mon.user.first_name)
        if timetable_mon:
            timetables['t_mon_dict'] = {'first_name': timetable_mon.user.first_name,
                                        'last_name': timetable_mon.user.last_name,
                                        'image': timetable_mon.user.image}
        if timetable_eve:
            timetables['t_eve_dict'] = {'first_name': timetable_eve.user.first_name,
                                        'last_name': timetable_eve.user.last_name,
                                        'image': timetable_eve.user.image}
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
