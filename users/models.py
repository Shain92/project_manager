from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""
    
    USER_TYPE_CHOICES = [
        ('НПТО', 'НПТО'),
        ('ПТО', 'ПТО'),
        ('Директор', 'Директор'),
        ('Снабжение', 'Снабжение'),
        ('Админ', 'Админ'),
        ('Гость', 'Гость'),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='Гость',
        verbose_name='Тип пользователя'
    )
    
    def is_guest(self):
        """Проверка, является ли пользователь гостем"""
        return self.user_type == 'Гость'
