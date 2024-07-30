"""
Модуль содержит класс DataAccess для управления доступом к данным и выполнения операций с моделями.
"""
from datetime import datetime

from django.db import transaction
from django.db.models import Q

from admins.models import Branch, BranchUser
from masters.models import Timetable
from users.models import User


class DataAccess:
    """
    Класс для доступа к данным и выполнения операций с моделями.
    """
    _instance = None

    def __new__(cls, *args: tuple, **kwargs: dict):
        """
        Контролирует, чтобы был только один объект класса.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def get_timetables(branch_id: int, date: str):
        """
        Возвращает расписания для указанного филиала и даты.

        Args:
            branch_id (int): Идентификатор филиала.
            date (str): Дата расписания.

        Returns:
            QuerySet: Список расписаний.
        """
        return Timetable.objects.filter(branch=branch_id, date=date).all()

    @staticmethod
    def get_user(user_id: int):
        """
        Возвращает пользователя по идентификатору.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            User: Объект пользователя.
        """
        return User.objects.get(id=user_id)

    @staticmethod
    def get_branch(branch_id: int):
        """
        Возвращает филиал по идентификатору.

        Args:
            branch_id (int): Идентификатор филиала.

        Returns:
            Branch: Объект филиала.
        """
        return Branch.objects.get(id=branch_id)

    @staticmethod
    def get_branches_user(user: User):
        """
        Возвращает филиалы, к которым принадлежит пользователь.

        Args:
            user (User): Объект пользователя.

        Returns:
            QuerySet: Список филиалов.
        """
        return Branch.objects.filter(branchuser__user=user)

    @staticmethod
    def get_masters(branch_id: int):
        """
        Возвращает мастеров, работающих в указанном филиале.

        Args:
            branch_id (int): Идентификатор филиала.

        Returns:
            QuerySet: Список мастеров.
        """
        return User.objects.filter(branchuser__branch_id=branch_id)

    @staticmethod
    def add_branch_user(user: User, branches: list):
        """
        Добавляет пользователя к указанным филиалам.

        Args:
            user (User): Объект пользователя.
            branches (list): Список филиалов.
        """
        for branch in branches:
            BranchUser.objects.create(user=user, branch=branch)

    def get_timetables_data(self, branch_id: int, date: str) -> list:
        """
        Возвращает данные расписания для указанного филиала и даты.

        Args:
            branch_id (int): Идентификатор филиала.
            date (str): Дата расписания.

        Returns:
            list: Список расписаний.
        """
        timetables_list = []
        data_timetables = self.get_timetables(branch_id, date)
        quantity_chairs = self.get_branch(branch_id).chairs
        for chair in range(1, quantity_chairs + 1):
            timetables = {}
            timetable_mon = data_timetables.filter(chair_number=chair, shift_mon=True).first()
            timetable_eve = data_timetables.filter(chair_number=chair, shift_eve=True).first()
            timetables['num'] = chair
            if timetable_mon:
                timetables['t_mon_dict'] = {
                    'first_name': timetable_mon.user.first_name,
                    'last_name': timetable_mon.user.last_name,
                    'image': timetable_mon.user.image,
                    'id': timetable_mon.user.id
                }
            if timetable_eve:
                timetables['t_eve_dict'] = {
                    'first_name': timetable_eve.user.first_name,
                    'last_name': timetable_eve.user.last_name,
                    'image': timetable_eve.user.image,
                    'id': timetable_eve.user.id
                }
            timetables_list.append(timetables)
        return timetables_list

    def add_or_update_timetable_shift(self, branch_id: int, user_id: int, chair_num: int, date: str, shift_type: str):
        """
        Добавляет или обновляет смену в расписании.

        Args:
            branch_id (int): Идентификатор филиала.
            user_id (int): Идентификатор пользователя.
            chair_num (int): Номер кресла.
            date (str): Дата расписания.
            shift_type (str): Тип смены ('mon' или 'eve').
        """
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

    def delete_timetable_shift(self, branch_id: int, user_id: int, chair_num: int, date: str, shift_type: str):
        """
        Удаляет смену из расписания.

        Args:
            branch_id (int): Идентификатор филиала.
            user_id (int): Идентификатор пользователя.
            chair_num (int): Номер кресла.
            date (str): Дата расписания.
            shift_type (str): Тип смены ('mon' или 'eve').
        """
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
            except Timetable.DoesNotExist:
                print("Запись не найдена.")

    @staticmethod
    def timetables_month(user: User, first_day: datetime, last_day: datetime):
        """
        Возвращает расписания пользователя за указанный месяц.

        Args:
            user (User): Объект пользователя.
            first_day (datetime): Первый день месяца.
            last_day (datetime): Последний день месяца.

        Returns:
            QuerySet: Список расписаний.
        """
        return Timetable.objects.filter(
            Q(user=user) &
            Q(date__gte=first_day) &
            Q(date__lte=last_day)
        ).order_by('date')