from django.shortcuts import render


def index(request):
    context = {
        'title': 'masters',
    }
    return render(request, 'index.html', context)
