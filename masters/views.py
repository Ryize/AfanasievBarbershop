from datetime import datetime

from django.shortcuts import render

from admins.models import Branch


def index(request):
    context = {
        'title': 'masters',
        'branches': Branch.objects.all(),
    }
    return render(request, 'index.html', context)


def schedule(request, branch_id, date):
    context = {
        'title': 'schedule',
        'branches': Branch.objects.all(),
        'chairs': Branch.objects.get(id=branch_id).chairs,
        'address': Branch.objects.get(id=branch_id).address,
        'date': format_date(date),
    }
    return render(request, 'schedule.html', context)


def format_date(date):
    date = datetime.strptime(date, '%Y-%m-%d')

    months = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]

    formatted_date = f"{date.day} {months[date.month - 1]} {date.year}"

    return formatted_date
