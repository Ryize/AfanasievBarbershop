"""
Модуль содержит модель для управления расписанием.
"""

from django.db import models

from admins.models import Branch
from users.models import User


class Timetable(models.Model):
    """
    Модель для представления расписания.

    Attributes:
        branch (Branch): Ссылка на модель Branch.
        user (User): Ссылка на модель User.
        chair_number (int): Номер кресла.
        date (date): Дата расписания.
        shift_mon (bool): Флаг утренней смены.
        shift_eve (bool): Флаг вечерней смены.
    """
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chair_number = models.PositiveIntegerField(default=1)
    date = models.DateField()
    shift_mon = models.BooleanField(default=False)
    shift_eve = models.BooleanField(default=False)

    def __str__(self) -> str:
        """
        Возвращает строковое представление расписания.

        Returns:
            str: Пользователь, филиал и дата расписания.
        """
        return f"{self.user} - {self.branch} - {self.date}"
