from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import UserProfileForm

from services.business_logic import BusinessLogic, staff_required
from services.data_access import DataAccess

logic = BusinessLogic()
dataAccess = DataAccess()


@staff_required
def index(request):
    context = {
        'title': 'admins',
        'branches': dataAccess.get_branches_user(request.user),
    }
    return render(request, 'admins/index.html', context)


@staff_required
def all_masters(request, branch_id):
    context = {
        'title': 'all_masters',
        'branches': dataAccess.get_branches_user(request.user),
        'address': dataAccess.get_branch(branch_id),
        'masters': dataAccess.get_masters(branch_id),
    }
    return render(request, 'admins/all_masters.html', context)


@staff_required
def master(request, branch_id, master_id):
    user = dataAccess.get_user(master_id)
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
               'branches': dataAccess.get_branches_user(request.user),
               'address': dataAccess.get_branch(branch_id),
               'form': form}
    return render(request, 'admins/master_profile.html', context)


@staff_required
def del_master(request, branch_id, master_id):
    user = dataAccess.get_user(master_id)
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
            dataAccess.add_or_update_timetable_shift(
                branch_id=int(branch_id),
                user_id=user_id,
                chair_num=chair_num,
                date=date,
                shift_type=shift_type
            )
        elif action == 'del':
            dataAccess.delete_timetable_shift(
                branch_id=int(branch_id),
                user_id=user_id,
                chair_num=chair_num,
                date=date,
                shift_type=shift_type
            )

    quantity_chairs = dataAccess.get_branch(branch_id).chairs
    context = {
        'title': 'Расписание',
        'branches': dataAccess.get_branches_user(request.user),
        'chairs': quantity_chairs,
        'address': dataAccess.get_branch(branch_id),
        'branch_id': dataAccess.get_branch(branch_id).id,
        'date': date,
        'format_date': logic.format_date(date),
        'timetables_data': dataAccess.get_timetables_data(branch_id, date),
        'masters': dataAccess.get_masters(branch_id)
    }

    return render(request, 'admins/schedule_admin.html', context)

