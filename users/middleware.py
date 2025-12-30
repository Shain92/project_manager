from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    """Middleware для защиты всех страниц паролем"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Исключения для статических файлов и медиа
        if request.path.startswith(settings.STATIC_URL) or \
           request.path.startswith('/media/'):
            return self.get_response(request)
        
        # Исключения для страниц входа, регистрации и админки
        exempt_paths = ['/login/', '/register/', '/admin/login/', '/admin/logout/']
        is_exempt = any(request.path.startswith(path) for path in exempt_paths)
        
        # Проверка авторизации для всех остальных страниц
        if not request.user.is_authenticated and not is_exempt:
            return redirect('users:login')
        
        # Ограничение доступа для гостей (только главная страница)
        # Суперпользователи имеют доступ ко всем страницам
        if request.user.is_authenticated and not request.user.is_superuser and hasattr(request.user, 'is_guest'):
            if request.user.is_guest() and not is_exempt and request.path != '/':
                return redirect('users:home')
        
        response = self.get_response(request)
        return response

