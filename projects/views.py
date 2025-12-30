from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os
from .models import Project, Note, NoteStatus, NoteFile
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
    notes = Note.objects.filter(project=project).select_related('author').prefetch_related('files').order_by('-created_at')
    
    notes_data = []
    for note in notes:
        files_data = []
        for file_obj in note.files.all():
            files_data.append({
                'id': file_obj.id,
                'original_name': file_obj.original_name,
                'file_size': file_obj.file_size,
                'file_size_display': file_obj.get_file_size_display(),
                'uploaded_at': file_obj.uploaded_at.strftime('%d.%m.%Y %H:%M'),
            })
        
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
            'files': files_data,
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


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def upload_note_file(request, note_id):
    """Загрузить файл к заметке"""
    try:
        note = get_object_or_404(Note, id=note_id)
        
        if 'file' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'Файл не предоставлен'}, status=400)
        
        uploaded_file = request.FILES['file']
        file_size = uploaded_file.size
        
        # Проверка размера файла (50 МБ)
        max_size = 50 * 1024 * 1024  # 50 МБ в байтах
        if file_size > max_size:
            return JsonResponse({'success': False, 'error': 'Размер файла превышает 50 МБ'}, status=400)
        
        note_file = NoteFile.objects.create(
            note=note,
            file=uploaded_file,
            original_name=uploaded_file.name,
            file_size=file_size,
            uploaded_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'file': {
                'id': note_file.id,
                'original_name': note_file.original_name,
                'file_size': note_file.file_size,
                'file_size_display': note_file.get_file_size_display(),
                'uploaded_at': note_file.uploaded_at.strftime('%d.%m.%Y %H:%M'),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def download_note_file(request, file_id):
    """Скачать файл заметки"""
    try:
        note_file = get_object_or_404(NoteFile, id=file_id)
        
        if not note_file.file:
            raise Http404("Файл не найден")
        
        file_path = note_file.file.path
        if not os.path.exists(file_path):
            raise Http404("Файл не найден на сервере")
        
        response = FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=note_file.original_name
        )
        return response
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def delete_note_file(request, file_id):
    """Удалить файл заметки"""
    try:
        note_file = get_object_or_404(NoteFile, id=file_id)
        
        # Удалить физический файл
        if note_file.file:
            file_path = note_file.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
        
        note_file.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
