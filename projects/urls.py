from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.list_projects, name='list'),
]

