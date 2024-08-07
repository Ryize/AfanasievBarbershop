"""
Модуль содержит модель для управления расписанием.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

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
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Филиал'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Мастер'))
    chair_number = models.PositiveIntegerField(default=1, verbose_name=_('Номер кресла'))
    date = models.DateField(verbose_name=_('Дата'))
    shift_mon = models.BooleanField(default=False, verbose_name=_('Утренняя смена'))
    shift_eve = models.BooleanField(default=False, verbose_name=_('Вечерняя смена'))

    class Meta:
        verbose_name = _('Расписание')
        verbose_name_plural = _('Расписание')

    def __str__(self) -> str:
        """
        Возвращает строковое представление расписания.

        Returns:
            str: Пользователь, филиал и дата расписания.
        """
        return f"{self.user} - {self.branch} - {self.date}"
