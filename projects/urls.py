from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.list_projects, name='list'),
    path('notes/<int:project_id>/', views.get_notes, name='get_notes'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:note_id>/update/', views.update_note, name='update_note'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('notes/<int:note_id>/files/upload/', views.upload_note_file, name='upload_note_file'),
    path('files/<int:file_id>/download/', views.download_note_file, name='download_note_file'),
    path('files/<int:file_id>/delete/', views.delete_note_file, name='delete_note_file'),
    path('requirements/<int:project_id>/', views.get_requirements, name='get_requirements'),
    path('requirements/create/', views.create_requirement, name='create_requirement'),
    path('requirements/<int:requirement_id>/update/', views.update_requirement, name='update_requirement'),
    path('requirements/<int:requirement_id>/delete/', views.delete_requirement, name='delete_requirement'),
    path('requirements/<int:requirement_id>/files/upload/', views.upload_requirement_file, name='upload_requirement_file'),
    path('requirement-files/<int:file_id>/download/', views.download_requirement_file, name='download_requirement_file'),
    path('requirement-files/<int:file_id>/delete/', views.delete_requirement_file, name='delete_requirement_file'),
]

