from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Branch

from services.business_logic import BusinessLogic

logic = BusinessLogic()


@login_required
def index(request):
    context = {
        'title': 'masters',
        'branches': Branch.objects.filter(branchuser__user=request.user),
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
            logic.add_or_update_timetable_shift(
                branch_id=int(branch_id),
                user_id=request.user.id,
                chair_num=chair_num,
                date=date,
                shift_type=shift_type
            )
        elif action == 'del':
            logic.delete_timetable_shift(
                branch_id=int(branch_id),
                user_id=request.user.id,
                chair_num=chair_num,
                date=date,
                shift_type=shift_type
            )

    quantity_chairs = Branch.objects.get(id=branch_id).chairs
    context = {
        'title': 'Расписание',
        'branches': Branch.objects.filter(branchuser__user=request.user),
        'chairs': quantity_chairs,
        'address': Branch.objects.get(id=branch_id).address,
        'branch_id': Branch.objects.get(id=branch_id).id,
        'date': date,
        'format_date': logic.format_date(date),
        'timetables_data': logic.get_timetables_data(branch_id, date),
        'total_hours_in_month': logic.total_hours_in_month(request.user),
        'hours_worked_in_month': logic.hours_worked_in_month(request.user)
    }

    return render(request, 'schedule.html', context)
