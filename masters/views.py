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
        'date': date,
    }
    return render(request, 'schedule.html', context)
