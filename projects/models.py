from django.db import models
from django.conf import settings


class ProjectStatus(models.Model):
    """Модель статуса проекта"""
    name = models.CharField(max_length=100, verbose_name='Название')
    color = models.CharField(max_length=7, verbose_name='Цвет (HEX)', help_text='Формат: #RRGGBB')

    class Meta:
        verbose_name = 'Статус проекта'
        verbose_name_plural = 'Статусы проектов'
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    """Модель проекта"""
    name = models.CharField(max_length=200, verbose_name='Имя')
    cipher = models.CharField(max_length=50, verbose_name='Шифр')
    code = models.CharField(max_length=50, verbose_name='Код')
    responsible = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects',
        verbose_name='Ответственный'
    )
    completion_percent = models.IntegerField(
        default=0,
        verbose_name='% готовности',
        help_text='Процент готовности проекта (0-100)'
    )
    note = models.TextField(blank=True, verbose_name='Примечание')
    status = models.ForeignKey(
        ProjectStatus,
        on_delete=models.PROTECT,
        related_name='projects',
        verbose_name='Статус'
    )
    construction_site = models.ForeignKey(
        'building_sites.BuildingSite',
        on_delete=models.PROTECT,
        related_name='projects',
        verbose_name='Строительный участок'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
