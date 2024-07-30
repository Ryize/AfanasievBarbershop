from datetime import datetime, timedelta

from django.db import transaction
from django.db.models import Q

from admins.models import Branch
from masters.models import Timetable
from users.models import User


class BusinessLogic:
    @staticmethod
    def get_timetables_data(branch_id, date):
        timetables_list = []
        data_timetables = Timetable.objects.filter(branch=branch_id, date=date).all()
        quantity_chairs = Branch.objects.get(id=branch_id).chairs
        for chair in range(1, quantity_chairs + 1):
            timetables = {}
            timetable_mon = data_timetables.filter(chair_number=chair, shift_mon=True).first()
            timetable_eve = data_timetables.filter(chair_number=chair, shift_eve=True).first()
            timetables['num'] = chair
            if timetable_mon:
                timetables['t_mon_dict'] = {'first_name': timetable_mon.user.first_name,
                                            'last_name': timetable_mon.user.last_name,
                                            'image': timetable_mon.user.image,
                                            'id': timetable_mon.user.id}
            if timetable_eve:
                timetables['t_eve_dict'] = {'first_name': timetable_eve.user.first_name,
                                            'last_name': timetable_eve.user.last_name,
                                            'image': timetable_eve.user.image,
                                            'id': timetable_eve.user.id}
            timetables_list.append(timetables)
        return timetables_list

    @staticmethod
    def format_date(date):
        date = datetime.strptime(date, '%Y-%m-%d')

        months = [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
        ]

        formatted_date = f"{date.day} {months[date.month - 1]} {date.year}"

        return formatted_date

    @staticmethod
    def get_user(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def get_branch(branch_id):
        return Branch.objects.get(id=branch_id)

    def add_or_update_timetable_shift(self, branch_id, user_id, chair_num, date, shift_type):
        branch = self.get_branch(branch_id)
        user = self.get_user(user_id)
        defaults = {'shift_mon': shift_type == 'mon', 'shift_eve': shift_type == 'eve'}
        with transaction.atomic():
            timetable, created = Timetable.objects.get_or_create(
                branch=branch,
                user=user,
                chair_number=chair_num,
                date=date,
                defaults=defaults
            )
            if not created:
                if shift_type == 'mon':
                    timetable.shift_mon = True
                elif shift_type == 'eve':
                    timetable.shift_eve = True
                timetable.save()

    def delete_timetable_shift(self, branch_id, user_id, chair_num, date, shift_type):
        branch = self.get_branch(branch_id)
        user = self.get_user(user_id)
        with transaction.atomic():
            try:
                timetable = Timetable.objects.get(
                    branch=branch,
                    user=user,
                    chair_number=chair_num,
                    date=date
                )
                if shift_type == 'mon':
                    if timetable.shift_mon and timetable.shift_eve:
                        timetable.shift_mon = False
                        timetable.save()
                    else:
                        timetable.delete()
                elif shift_type == 'eve':
                    if timetable.shift_mon and timetable.shift_eve:
                        timetable.shift_eve = False
                        timetable.save()
                    else:
                        timetable.delete()

                print("Запись успешно удалена.")
            except Timetable.DoesNotExist:
                print("Запись не найдена.")

    @staticmethod
    def get_first_day():
        current_date = datetime.now()
        return current_date.replace(day=1)

    @staticmethod
    def calculate_hours(user, last_day, first_day):

        hours = 0

        timetable_records = Timetable.objects.filter(
            Q(user=user) &
            Q(date__gte=first_day) &
            Q(date__lte=last_day)
        )
        for _ in timetable_records:
            if _.shift_mon:
                hours += 8
            if _.shift_eve:
                hours += 5
        return hours

    def total_hours_in_month(self, user):
        first_day = self.get_first_day()
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        hours = self.calculate_hours(user, last_day, first_day)
        return hours

    def hours_worked_in_month(self, user):
        first_day = self.get_first_day()
        last_day = datetime.now() - timedelta(days=1)
        hours = self.calculate_hours(user, last_day, first_day)
        return hours

    def user_timetable_month(self, user):
        timetable_month = []
        first_day = self.get_first_day()
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        timetable_records = Timetable.objects.filter(
            Q(user=user) &
            Q(date__gte=first_day) &
            Q(date__lte=last_day)
        )

        for timetable_record in timetable_records:
            timetable_day = {'date': timetable_record.date.strftime("%d.%m.%Y"),
                             'branch': timetable_record.branch.address,
                             'chair_number': timetable_record.chair_number}
            if timetable_record.shift_mon and timetable_record.shift_eve:
                timetable_day['start_time'] = '9:00'
                timetable_day['end_time'] = '20:00'
            elif timetable_record.shift_mon:
                timetable_day['start_time'] = '9:00'
                timetable_day['end_time'] = '15:00'
            elif timetable_record.shift_eve:
                timetable_day['start_time'] = '15:00'
                timetable_day['end_time'] = '20:00'
            timetable_month.append(timetable_day)
        return timetable_month
