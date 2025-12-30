from django.contrib import admin
from .models import BuildingSite


@admin.register(BuildingSite)
class BuildingSiteAdmin(admin.ModelAdmin):
    """Админка для строительных участков"""
    list_display = ['name', 'manager', 'description']
    search_fields = ['name', 'description']
    list_filter = ['manager']
    fields = ('name', 'description', 'manager')
