from django.shortcuts import render


def all_masters(request):
    return render(request, 'admins/admin_all_masters.html')


def left_panel(request):
    return render(request, 'admins/admin_base_with_left_panel.html')