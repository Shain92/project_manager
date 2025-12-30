from django.db import models
from django.conf import settings


class BuildingSite(models.Model):
    """Модель строительного участка"""
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='building_sites',
        verbose_name='Начальник участка'
    )

    class Meta:
        verbose_name = 'Строительный участок'
        verbose_name_plural = 'Строительные участки'
        ordering = ['name']

    def __str__(self):
        return self.name
