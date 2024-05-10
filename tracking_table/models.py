from django.db import models


class Table(models.Model):
    login = models.CharField(max_length=32, unique=True, verbose_name='Логин')
    description = models.TextField(verbose_name='Описание')
    status = models.BooleanField(default=False, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.login} ({self.status})'

    class Meta:
        verbose_name = 'Таблица'
        verbose_name_plural = 'Таблицы'
