from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from admins.models import Branch, BranchUser

# Register your models here.
admin.site.register(Branch)
admin.site.register(BranchUser)

admin.site.site_header = _("Администрирование сайта")
admin.site.site_title = _("Админка")
admin.site.index_title = _("Добро пожаловать в админку")