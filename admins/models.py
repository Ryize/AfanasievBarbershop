"""
Модуль содержит модели для управления филиалами и их пользователями.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Branch(models.Model):
    """
    Модель для представления филиала.

    Attributes:
        name (str): Название филиала.
        address (str): Адрес филиала.
        chairs (int): Количество кресел в филиале.
    """
    name = models.CharField(_('Филиал'), max_length=100)
    address = models.CharField(_('Адрес'), max_length=255)
    chairs = models.PositiveIntegerField(_('Колличество стульев'))

    class Meta:
        verbose_name = _('Филиал')
        verbose_name_plural = _('Филиалы')

    def __str__(self) -> str:
        """
        Возвращает строковое представление адреса филиала.

        Returns:
            str: Адрес филиала.
        """
        return self.address


class BranchUser(models.Model):
    """
    Модель для представления связи между филиалом и пользователем.

    Attributes:
        branch (Branch): Ссылка на модель Branch.
        user (User): Ссылка на модель User.
    """
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Филиал'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))

    class Meta:
        verbose_name = _('Связь пользователь-филиал')
        verbose_name_plural = _('Связь пользователь-филиал')

    def __str__(self) -> str:
        """
        Возвращает строковое представление связи пользователя и филиала.

        Returns:
            str: Пользователь и филиал.
        """
        return f"{self.user} - {self.branch}"
