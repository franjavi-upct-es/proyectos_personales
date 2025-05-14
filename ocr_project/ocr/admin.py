from django.contrib import admin
from .models import Albaran

@admin.register(Albaran)
class AlbaranAdmin(admin.ModelAdmin):
    list_display = ('archivo', 'numero', 'fecha', 'proveedor', 'total', 'creado_en')
