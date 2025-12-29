from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project


@login_required
def list_projects(request):
    """Список проектов"""
    projects = Project.objects.select_related('status').prefetch_related('responsible').all()
    return render(request, 'projects/list.html', {'projects': projects})
