from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from authentication.models import CustomUser


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    chairs = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class BranchUser(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.branch}"