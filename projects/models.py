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


class NoteStatus(models.TextChoices):
    """Статусы заметок"""
    IN_WORK = 'in_work', 'В работе'
    ON_REVIEW = 'on_review', 'На проверке'
    FIXING = 'fixing', 'Исправление'
    DONE = 'done', 'Сдано'


class Note(models.Model):
    """Модель заметки проекта"""
    STATUS_COLORS = {
        NoteStatus.IN_WORK: '#FFC107',  # Желтый
        NoteStatus.ON_REVIEW: '#2196F3',  # Синий
        NoteStatus.FIXING: '#9C27B0',  # Фиолетовый
        NoteStatus.DONE: '#4CAF50',  # Зеленый
    }
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Проект'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='notes',
        verbose_name='Автор'
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    status = models.CharField(
        max_length=20,
        choices=NoteStatus.choices,
        default=NoteStatus.IN_WORK,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_status_color(self):
        """Получить цвет статуса"""
        return self.STATUS_COLORS.get(self.status, '#667eea')