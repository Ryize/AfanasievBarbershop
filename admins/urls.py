from django.urls import path

from admins.views import index, all_masters, schedule, master, del_master

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('all_masters/<int:branch_id>/', all_masters, name='all_masters'),
    path('schedule/<int:branch_id>/<str:date>/', schedule, name='schedule'),
    path('master/<int:branch_id>/<int:master_id>/', master, name='master'),
    path('del_master/<int:branch_id>/<int:master_id>/', del_master, name='del_master')
]
