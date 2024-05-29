from django.shortcuts import render


def all_masters(request):
    return render(request, 'admins/admin_all_masters.html')