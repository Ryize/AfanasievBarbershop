from django.urls import path
from .views import index, register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", index, name="index"),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html'), name='login'),
]