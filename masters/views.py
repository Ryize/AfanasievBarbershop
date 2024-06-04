from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        'title': 'masters',
    }
    return render(request, 'masters/index.html', context)