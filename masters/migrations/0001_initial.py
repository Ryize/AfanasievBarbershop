# Generated by Django 4.2.13 on 2024-06-09 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chair_number', models.PositiveIntegerField(default=1)),
                ('date', models.DateField()),
                ('shift_mon', models.BooleanField(default=False)),
                ('shift_eve', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins.branch')),
            ],
        ),
    ]