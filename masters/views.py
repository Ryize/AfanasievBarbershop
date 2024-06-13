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
    context = {
        'title': 'Расписание',
        'branches': Branch.objects.all(),
        'chairs': Branch.objects.get(id=branch_id).chairs,
        'address': Branch.objects.get(id=branch_id).address,
        'date': format_date(date),
    }
    return render(request, 'schedule.html', context)


@login_required
def update_timetable(request):
    if request.method == 'POST':
        branch_id = request.POST.get('branch_id')
        chair_number = request.POST.get('chair_number')
        date = request.POST.get('date')
        shift_type = request.POST.get('shift_type')

        branch = Branch.objects.get(id=branch_id)
        user = request.user

        timetable, created = Timetable.objects.get_or_create(
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
