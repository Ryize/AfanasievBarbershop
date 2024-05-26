from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser, ):
    ROLE_CHOICES = [
        ('director', 'Директор'),
        ('administrator', 'Администратор'),
        ('master', 'Мастер'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    branch = models.ForeignKey('admins.Branch', on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def is_director(self):
        return self.role == 'director'

    def is_administrator(self):
        return self.role == 'administrator'

    def is_master(self):
        return self.role == 'master'
