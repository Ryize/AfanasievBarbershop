from django.urls import path

from authentication.views import index, login_view

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login')
]