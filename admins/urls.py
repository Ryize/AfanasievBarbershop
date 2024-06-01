from django.urls import path

from admins.views import all_masters, left_panel


urlpatterns = [
    path('all_masters/', all_masters, name='all_masters'),
    path('left_panel/', left_panel, name='left_panel'),
]