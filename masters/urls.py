from django.urls import path
from masters.views import index, schedule


app_name = 'masters'

urlpatterns = [
    path('', index, name='index'),
    path('schedule/<int:branch_id>/<str:date>/', schedule, name='schedule'),
]