from django.urls import path
from masters.views import index


urlpatterns = [
    path('', index, name='index'),
]