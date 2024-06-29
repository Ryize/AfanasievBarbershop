from django.shortcuts import render
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
        'address': Branch.objects.get(id=branch_id).address,
        'masters': User.objects.filter(branchuser__branch_id=branch_id)
    }
    return render(request, 'admins/all_masters.html', context)
