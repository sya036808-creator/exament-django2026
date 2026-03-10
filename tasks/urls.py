from django.urls import path
from . import views

# Définition des routes (URLs) pour l'application tasks
urlpatterns = [
    # Tableau de bord principal
    path('', views.dashboard, name='dashboard'),
    
    # Routes pour la gestion des projets (CRUD)
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    
    # Routes pour la gestion des tâches
    path('projects/<int:project_pk>/tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    
    # Route pour l'affichage des statistiques et primes
    path('statistics/', views.statistics_view, name='statistics'),
]
