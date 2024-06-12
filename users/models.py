from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.core.exceptions import ValidationError
import re


def validate_phone_number(value):
    phone_regex = re.compile(r'^\+?1?\d{9,15}$')
    if not phone_regex.match(value):
        raise ValidationError(
            'Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
        )


class PhoneNumberField(models.CharField):
    default_validators = [validate_phone_number]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15
        super().__init__(*args, **kwargs)


class User(AbstractUser):
    username = PhoneNumberField(unique=True)
    image = models.ImageField(upload_to='user_images', default='default.jpg')

