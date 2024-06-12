from django.db import models

from admins.models import Branch
from users.models import User


class Timetable(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chair_number = models.PositiveIntegerField(default=1)
    date = models.DateField()
    shift_mon = models.BooleanField(default=False)
    shift_eve = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.branch} - {self.date}"
