from django.urls import path

from users.views import login, logout, profile, register

app_name = 'users'

urlpatterns = [
    path('', login, name='login'),
    path('register/<int:branch_id>', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
]
