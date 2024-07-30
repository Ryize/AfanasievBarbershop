from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from services.data_access import DataAccess

dataAccess = DataAccess()


def staff_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Доступно только администратору!')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


class BusinessLogic:

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
    def get_first_day():
        current_date = datetime.now()
        return current_date.replace(day=1)

    @staticmethod
    def calculate_hours(user, last_day, first_day):

        hours = 0

        timetable_records = dataAccess.timetables_month(user, first_day, last_day)

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

        timetable_records = dataAccess.timetables_month(user, first_day, last_day)

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
