from django.apps import AppConfig


class TrackingTableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracking_table'
    verbose_name = 'Таблица посещений'
