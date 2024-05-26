from django.db import models

from admins.models import Branch
from authentication.models import CustomUser


class WorkSchedule(models.Model):
    master = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date = models.DateField()
    shift_morning = models.BooleanField(default=False)
    shift_evening = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.master.username} - {self.date} - Morning: {self.shift_morning}, Evening: {self.shift_evening}'
