from django.shortcuts import render
from .models import Branch


def index(request):
    context = {
        'title': 'admins',
        'branches': Branch.objects.filter(branchuser__user=request.user)
    }
    return render(request, 'admins/index.html', context)


def all_masters(request):
    context = {
        'title': 'all_masters',
        'branches': Branch.objects.filter(branchuser__user=request.user)
    }
    return render(request, 'admins/all_masters.html', context)
