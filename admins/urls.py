from django.urls import path

from admins.views import all_masters


urlpatterns = [
    path('all_masters/', all_masters, name='all_masters')
]