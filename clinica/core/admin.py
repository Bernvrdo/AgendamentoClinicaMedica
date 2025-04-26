from django.contrib import admin
from .models import User, Agenda, Consulta
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('tipo', 'especialidade')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Agenda)
admin.site.register(Consulta)
