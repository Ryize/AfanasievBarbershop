from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Timetable, Branch


def index(request):
    context = {
        'title': 'masters',
        'branches': Branch.objects.all(),
    }
    return render(request, 'index.html', context)


def schedule(request, branch_id, date):
    timetables_list = []
    quantity_chairs = Branch.objects.get(id=branch_id).chairs
    data_timetables = Timetable.objects.filter(branch=branch_id, date=date).all()

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
            timetables['t_eve_dict'] = {'first_name': timetable_mon.user.first_name,
                                        'last_name': timetable_mon.user.last_name,
                                        'image': timetable_mon.user.image}
        timetables_list.append(timetables)
    print(timetables_list)

    context = {
        'title': 'Расписание',
        'branches': Branch.objects.all(),
        'chairs': quantity_chairs,
        'address': Branch.objects.get(id=branch_id).address,
        'date': date,
        'format_date': format_date(date),
        'timetables_data': timetables_list,
    }

    return render(request, 'schedule.html', context)


@login_required
def update_timetable(request):
    if request.method == 'POST':
        branch_id = request.POST.get('branch_id')
        chair_number = request.POST.get('chair_number')
        date = request.POST.get('date')
        shift_type = request.POST.get('shift_type')
        print(branch_id)
        branch = Branch.objects.get(id=branch_id)
        user = request.user

        timetable = Timetable.objects.create(
            branch=branch,
            user=user,
            chair_number=chair_number,
            date=date
        )

        if shift_type == 'mon':
            timetable.shift_mon = True
        elif shift_type == 'eve':
            timetable.shift_eve = True

        timetable.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def format_date(date):
    date = datetime.strptime(date, '%Y-%m-%d')

    months = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]

    formatted_date = f"{date.day} {months[date.month - 1]} {date.year}"

    return formatted_date
