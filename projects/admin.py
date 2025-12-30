from django.contrib import admin
from .models import Project, ProjectStatus, Note


@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    """Админка для статусов проектов"""
    list_display = ['name', 'color']
    search_fields = ['name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Админка для проектов"""
    list_display = ['name', 'cipher', 'code', 'status', 'construction_site', 'completion_percent', 'created_at']
    list_filter = ['status', 'construction_site', 'created_at']
    search_fields = ['name', 'cipher', 'code']
    filter_horizontal = ['responsible']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'cipher', 'code', 'status', 'construction_site')
        }),
        ('Ответственные', {
            'fields': ('responsible',)
        }),
        ('Прогресс', {
            'fields': ('completion_percent',)
        }),
        ('Дополнительно', {
            'fields': ('note',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Админка для заметок"""
    list_display = ['title', 'project', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'project']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('project', 'author', 'title', 'description', 'status')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at')
        }),
    )
