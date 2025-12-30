from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project
from building_sites.models import BuildingSite


@login_required
def list_projects(request):
    """Список проектов"""
    building_sites = BuildingSite.objects.prefetch_related('projects__status').all()
    projects = Project.objects.select_related('status', 'construction_site').prefetch_related('responsible').all()
    return render(request, 'projects/list.html', {
        'building_sites': building_sites,
        'projects': projects
    })
