"""
Модуль содержит бизнес-логику и декораторы для управления доступом и расчетом рабочего времени.
"""

from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from services.data_access import DataAccess

# Инициализация доступа к данным.
dataAccess = DataAccess()


def staff_required(view_func):
    """
    Декоратор для проверки, является ли пользователь администратором.

    Args:
        view_func: Функция представления.

    Returns:
        функция представления или HTTP-ответ с кодом 403, если пользователь не администратор.
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Доступно только администратору!')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


class BusinessLogic:
    """
    Класс, содержащий бизнес-логику для управления расписанием и расчетом рабочего времени.
    """

    @staticmethod
    def format_date(date: str) -> str:
        """
        Форматирует дату в строку вида "день месяц год".

        Args:
            date (str): Дата в формате 'YYYY-MM-DD'.

        Returns:
            formatted_date(str): Форматированная дата.
        """
        date = datetime.strptime(date, '%Y-%m-%d')
        months = [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
        ]
        formatted_date = f'{date.day} {months[date.month - 1]} {date.year}'
        return formatted_date

    @staticmethod
    def get_first_day() -> datetime:
        """
        Возвращает первый день текущего месяца.

        Returns:
            datetime: Первый день текущего месяца.
        """
        current_date = datetime.now()
        return current_date.replace(day=1)

    @staticmethod
    def calculate_hours(user, last_day: datetime, first_day: datetime) -> int:
        """
        Рассчитывает количество часов работы пользователя за указанный период.

        Args:
            user: Пользователь.
            last_day (datetime): Последний день периода.
            first_day (datetime): Первый день периода.

        Returns:
            hours(int): Количество часов работы.
        """
        hours = 0
        timetable_records = dataAccess.timetables_month(user, first_day, last_day)
        for record in timetable_records:
            if record.shift_mon:
                hours += 8
            if record.shift_eve:
                hours += 5
        return hours

    def total_hours_in_month(self, user) -> int:
        """
        Рассчитывает общее количество часов работы пользователя за текущий месяц.

        Args:
            user: Пользователь.

        Returns:
            hours(int): Общее количество часов работы за текущий месяц.
        """
        first_day = self.get_first_day()
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        hours = self.calculate_hours(user, last_day, first_day)
        return hours

    def hours_worked_in_month(self, user) -> int:
        """
        Рассчитывает количество отработанных часов пользователя за текущий месяц до текущей даты.

        Args:
            user: Пользователь.

        Returns:
            hours(int): Количество отработанных часов за текущий месяц до текущей даты.
        """
        first_day = self.get_first_day()
        last_day = datetime.now() - timedelta(days=1)
        hours = self.calculate_hours(user, last_day, first_day)
        return hours

    def user_timetable_month(self, user) -> list:
        """
        Возвращает расписание пользователя за текущий месяц.

        Args:
            user: Пользователь.

        Returns:
            timetable_month(list): Расписание пользователя за текущий месяц.
        """
        timetable_month = []
        first_day = self.get_first_day()
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        timetable_records = dataAccess.timetables_month(user, first_day, last_day)
        for record in timetable_records:
            timetable_day = {
                'date': record.date.strftime("%d.%m.%Y"),
                'branch': record.branch.address,
                'chair_number': record.chair_number
            }
            if record.shift_mon and record.shift_eve:
                timetable_day['start_time'] = '9:00'
                timetable_day['end_time'] = '20:00'
            elif record.shift_mon:
                timetable_day['start_time'] = '9:00'
                timetable_day['end_time'] = '15:00'
            elif record.shift_eve:
                timetable_day['start_time'] = '15:00'
                timetable_day['end_time'] = '20:00'
            timetable_month.append(timetable_day)
        return timetable_month
