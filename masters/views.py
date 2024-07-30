from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from services.business_logic import BusinessLogic
from services.data_access import DataAccess

logic = BusinessLogic()
dataAccess = DataAccess()


@login_required
def index(request):
    context = {
        'title': 'masters',
        'branches': dataAccess.get_branches_user(request.user),
        'total_hours_in_month': logic.total_hours_in_month(request.user),
        'hours_worked_in_month': logic.hours_worked_in_month(request.user)
    }
    return render(request, 'index.html', context)


@login_required
def schedule(request, branch_id, date):
    if request.method == 'POST':
        action = request.POST['action']
        chair_num = request.POST.get('chair_num')
        shift_type = request.POST.get('shift_type')
        if action == 'add':
            dataAccess.add_or_update_timetable_shift(
                branch_id=int(branch_id),
                user_id=request.user.id,
                chair_num=chair_num,
                date=date,
                shift_type=shift_type
            )
        elif action == 'del':
            dataAccess.delete_timetable_shift(
                branch_id=int(branch_id),
                user_id=request.user.id,
                chair_num=chair_num,
                date=date,
                shift_type=shift_type
            )

    quantity_chairs = dataAccess.get_branch(branch_id).chairs
    context = {
        'title': 'Расписание',
        'branches': dataAccess.get_branches_user(request.user),
        'chairs': quantity_chairs,
        'address': dataAccess.get_branch(branch_id).address,
        'branch_id': dataAccess.get_branch(branch_id).id,
        'date': date,
        'format_date': logic.format_date(date),
        'timetables_data': dataAccess.get_timetables_data(branch_id, date),
        'total_hours_in_month': logic.total_hours_in_month(request.user),
        'hours_worked_in_month': logic.hours_worked_in_month(request.user)
    }

    return render(request, 'schedule.html', context)
