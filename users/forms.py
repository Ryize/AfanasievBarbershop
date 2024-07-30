"""
Модуль содержит формы для аутентификации и управления пользователями.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from admins.models import Branch
from users.models import User


class UserLoginForm(AuthenticationForm):
    """
    Форма для аутентификации пользователя.

    Attributes:
        username (str): Имя пользователя.
        password (str): Пароль пользователя.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'value': '+7'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control py-4'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя.

    Attributes:
        image (File): Изображение профиля пользователя.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        username (str): Имя пользователя.
        email (str): Email пользователя.
        password1 (str): Пароль пользователя.
        password2 (str): Повтор пароля пользователя.
        branches (QuerySet): Филиалы, к которым принадлежит пользователь.
    """
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Фамилия'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'value': '+7'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Повторите пароль'}))
    branches = forms.ModelMultipleChoiceField(
        queryset=Branch.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Выберите филиалы'
    )

    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    """
    Форма для изменения профиля пользователя.

    Attributes:
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        image (File): Изображение профиля пользователя.
        username (str): Имя пользователя.
        email (str): Email пользователя.
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')