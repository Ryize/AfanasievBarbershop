"""
Модуль содержит модели для управления филиалами и их пользователями.
"""

from django.db import models

from users.models import User


class Branch(models.Model):
    """
    Модель для представления филиала.

    Attributes:
        name (str): Название филиала.
        address (str): Адрес филиала.
        chairs (int): Количество кресел в филиале.
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    chairs = models.PositiveIntegerField()

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
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Возвращает строковое представление связи пользователя и филиала.

        Returns:
            str: Пользователь и филиал.
        """
        return f"{self.user} - {self.branch}"
