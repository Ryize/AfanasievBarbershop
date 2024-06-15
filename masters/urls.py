from django.urls import path
from masters.views import index, schedule, update_timetable

app_name = 'masters'

urlpatterns = [
    path('', index, name='index'),
    path('schedule/<int:branch_id>/<str:date>/', schedule, name='schedule'),
    path('schedule/', update_timetable, name='update_timetable'),
]