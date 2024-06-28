from django.urls import path

from admins.views import index, all_masters

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('all_masters/', all_masters, name='all_masters'),
]
