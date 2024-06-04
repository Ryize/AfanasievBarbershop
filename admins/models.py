from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    chairs = models.PositiveIntegerField()

    def __str__(self):
        return self.name
