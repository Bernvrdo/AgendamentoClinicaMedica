from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name')
    list_filter = ('user_type',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Consulta)
