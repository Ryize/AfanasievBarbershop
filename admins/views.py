from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import UserProfileForm
from .models import Branch, User
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from services.business_logic import BusinessLogic

logic = BusinessLogic()


def staff_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Доступно только администратору!')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@staff_required
def index(request):
    context = {
        'title': 'admins',
        'branches': Branch.objects.filter(branchuser__user=request.user)
    }
    return render(request, 'admins/index.html', context)


@staff_required
def all_masters(request, branch_id):
    context = {
        'title': 'all_masters',
        'branches': Branch.objects.filter(branchuser__user=request.user),
        'address': Branch.objects.get(id=branch_id),
        'masters': User.objects.filter(branchuser__branch_id=branch_id)
    }
    return render(request, 'admins/all_masters.html', context)


@staff_required
def master(request, branch_id, master_id):
    user = User.objects.get(id=master_id)
    if request.method == 'POST':
        form = UserProfileForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            redirect_url = reverse('admins:master', args=[branch_id, master_id])
            return HttpResponseRedirect(redirect_url)
    else:
        form = UserProfileForm(instance=user)
    context = {'title': 'Profile',
               'user': user,
               'total_hours_in_month': logic.total_hours_in_month(user),
               'hours_worked_in_month': logic.hours_worked_in_month(user),
               'timetable_month': logic.user_timetable_month(user),
               'branches': Branch.objects.filter(branchuser__user=request.user),
               'address': Branch.objects.get(id=branch_id),
               'form': form}
    return render(request, 'admins/master_profile.html', context)


@staff_required
def del_master(request, branch_id, master_id):
    user = User.objects.get(id=master_id)
    user.delete()
    redirect_url = reverse('admins:all_masters', args=[branch_id])
    return HttpResponseRedirect(redirect_url)


@staff_required
def schedule(request, branch_id, date):
    if request.method == 'POST':
        action = request.POST['action']
        chair_num = request.POST.get('chair_num')
        shift_type = request.POST.get('shift_type')
        user_id = request.POST.get('last_name')
        if action == 'add':
            logic.add_or_update_timetable_shift(
                branch_id=int(branch_id),
                user_id=user_id,
                chair_num=chair_num,
                date=date,
                shift_type=shift_type
            )
        elif action == 'del':
            logic.delete_timetable_shift(
                branch_id=int(branch_id),
                user_id=user_id,
                chair_num=chair_num,
                date=date,
                shift_type=shift_type
            )

    quantity_chairs = Branch.objects.get(id=branch_id).chairs
    context = {
        'title': 'Расписание',
        'branches': Branch.objects.filter(branchuser__user=request.user),
        'chairs': quantity_chairs,
        'address': Branch.objects.get(id=branch_id),
        'branch_id': Branch.objects.get(id=branch_id).id,
        'date': date,
        'format_date': logic.format_date(date),
        'timetables_data': logic.get_timetables_data(branch_id, date),
        'masters': User.objects.filter(branchuser__branch_id=branch_id)
    }

    return render(request, 'admins/schedule_admin.html', context)

