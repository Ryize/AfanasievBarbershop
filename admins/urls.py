from django.urls import path

from admins.views import index

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    # path('all_masters/', all_masters, name='all_masters'),
    # path('left_panel/', left_panel, name='left_panel'),
]