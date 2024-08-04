from django.contrib import admin

from admins.models import Branch, BranchUser

# Register your models here.
admin.site.register(Branch)
admin.site.register(BranchUser)
