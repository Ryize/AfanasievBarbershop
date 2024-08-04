"""
Модуль содержит модель пользователя с дополнительными полями.
"""

import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_phone_number(value: str) -> None:
    """
    Проверяет, соответствует ли номер телефона заданному формату.

    Args:
        value (str): Номер телефона.

    Raises:
        ValidationError: Если номер телефона не соответствует формату.
    """
    phone_regex = re.compile(r'^\+?1?\d{9,15}$')
    if not phone_regex.match(value):
        raise ValidationError(
            'Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
        )


class PhoneNumberField(models.CharField):
    """
    Поле для хранения и валидации номера телефона.

    Attributes:
        default_validators (list): Список валидаторов для номера телефона.
    """
    default_validators = [validate_phone_number]

    def __init__(self, *args: tuple, **kwargs: dict):
        """
        Инициализирует поле номера телефона с максимальной длиной 15 символов.

        Args:
            *args: Аргументы.
            **kwargs: Именованные аргументы.
        """
        kwargs['max_length'] = 15
        super().__init__(*args, **kwargs)


class User(AbstractUser):
    """
    Модель пользователя с дополнительными полями.

    Attributes:
        username (str): Номер телефона пользователя, используется как имя пользователя.
        image (ImageField): Изображение профиля пользователя.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
    """
    username = PhoneNumberField(unique=True)
    image = models.ImageField(upload_to='user_images', default='default.jpg')
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
