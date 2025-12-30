from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Project, Note, NoteStatus
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


@login_required
@require_http_methods(["GET"])
def get_notes(request, project_id):
    """Получить список заметок проекта"""
    project = get_object_or_404(Project, id=project_id)
    notes = Note.objects.filter(project=project).select_related('author').order_by('-created_at')
    
    notes_data = []
    for note in notes:
        notes_data.append({
            'id': note.id,
            'title': note.title,
            'description': note.description,
            'status': note.get_status_display(),
            'status_value': note.status,
            'status_color': note.get_status_color(),
            'author': note.author.username,
            'created_at': note.created_at.strftime('%d.%m.%Y %H:%M'),
            'updated_at': note.updated_at.strftime('%d.%m.%Y %H:%M'),
        })
    
    return JsonResponse({'notes': notes_data})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def create_note(request):
    """Создать новую заметку"""
    try:
        data = json.loads(request.body)
        project = get_object_or_404(Project, id=data.get('project_id'))
        
        note = Note.objects.create(
            project=project,
            author=request.user,
            title=data.get('title', ''),
            description=data.get('description', ''),
            status=data.get('status', NoteStatus.IN_WORK)
        )
        
        return JsonResponse({
            'success': True,
            'note': {
                'id': note.id,
                'title': note.title,
                'description': note.description,
                'status': note.get_status_display(),
                'status_value': note.status,
                'status_color': note.get_status_color(),
                'author': note.author.username,
                'created_at': note.created_at.strftime('%d.%m.%Y %H:%M'),
                'updated_at': note.updated_at.strftime('%d.%m.%Y %H:%M'),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def update_note(request, note_id):
    """Редактировать заметку"""
    try:
        note = get_object_or_404(Note, id=note_id)
        data = json.loads(request.body)
        
        if 'title' in data:
            note.title = data['title']
        if 'description' in data:
            note.description = data['description']
        if 'status' in data:
            note.status = data['status']
        
        note.save()
        
        return JsonResponse({
            'success': True,
            'note': {
                'id': note.id,
                'title': note.title,
                'description': note.description,
                'status': note.get_status_display(),
                'status_value': note.status,
                'status_color': note.get_status_color(),
                'author': note.author.username,
                'created_at': note.created_at.strftime('%d.%m.%Y %H:%M'),
                'updated_at': note.updated_at.strftime('%d.%m.%Y %H:%M'),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def delete_note(request, note_id):
    """Удалить заметку"""
    try:
        note = get_object_or_404(Note, id=note_id)
        note.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
