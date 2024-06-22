from django.shortcuts import render
from .models import Branch


def index(request):
    context = {
        'title': 'admins',
        'branches': Branch.objects.filter(branchuser__user=request.user)
    }
    return render(request, 'index.html', context)
