from django.contrib import admin

from tracking_table.models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    fields = ('login', 'description', 'status')
    list_display = ('login', 'status', 'created_at')
    list_display_links = ('login', 'created_at')
    list_filter = ('status', 'created_at',)
    readonly_fields = ('description',)
    empty_value_display = 'Поле пустое'
    list_per_page = 64
    list_max_show_all = 8
    list_editable = ('status',)
    search_fields = ('login',)
