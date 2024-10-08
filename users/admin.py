from django.contrib import admin

from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  fields = ('username', 'email', 'first_name', 'last_name', 'is_staff')
  list_display = ('username',)
  list_display_links = ('username',)
  empty_value_display = '-пустой-'
  list_per_page = 64
  list_max_show_all = 8

  def has_add_permission(self, request, obj=None):
      return False
