from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
import os
import uuid


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


def note_file_upload_path(instance, filename):
    """Генерация пути для загрузки файла заметки"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('notes', filename)


class NoteFile(models.Model):
    """Модель файла, прикрепленного к заметке"""
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Заметка'
    )
    file = models.FileField(
        upload_to=note_file_upload_path,
        verbose_name='Файл'
    )
    original_name = models.CharField(
        max_length=255,
        verbose_name='Оригинальное имя файла'
    )
    file_size = models.IntegerField(
        verbose_name='Размер файла (байт)'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Загружен'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='uploaded_files',
        verbose_name='Загрузил'
    )

    class Meta:
        verbose_name = 'Файл заметки'
        verbose_name_plural = 'Файлы заметок'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.original_name
    
    def get_file_size_display(self):
        """Получить размер файла в читаемом формате"""
        size = self.file_size
        for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} ТБ"
    
    def delete(self, *args, **kwargs):
        """Удалить файл с диска перед удалением записи"""
        if self.file:
            try:
                # Используем storage для удаления файла
                self.file.delete(save=False)
            except Exception:
                # Если storage не удалось удалить, пробуем через os
                try:
                    file_path = self.file.path
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except OSError:
                    pass  # Игнорируем ошибки удаления файла
        super().delete(*args, **kwargs)


@receiver(pre_delete, sender=NoteFile)
def delete_note_file(sender, instance, **kwargs):
    """Сигнал для удаления файла перед удалением записи NoteFile"""
    if instance.file:
        try:
            # Используем storage для удаления файла
            instance.file.delete(save=False)
        except Exception:
            # Если storage не удалось удалить, пробуем через os
            try:
                file_path = instance.file.path
                if os.path.exists(file_path):
                    os.remove(file_path)
            except OSError:
                pass  # Игнорируем ошибки удаления файла