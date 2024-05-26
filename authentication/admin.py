from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'role', 'branch', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email',
                       'phone', 'password1', 'password2', 'role',
                       'branch', 'avatar', 'is_staff', 'is_active'
                       )
        }
         ),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email', 'username')


admin.site.register(CustomUser, CustomUserAdmin)
