from django.urls import path

from admins.views import index, all_masters, schedule

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('all_masters/<int:branch_id>/', all_masters, name='all_masters'),
    path('schedule/<int:branch_id>/<str:date>/', schedule, name='schedule'),
]
