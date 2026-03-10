from django.urls import path
from . import views

# Définition des routes (URLs) pour l'application users
urlpatterns = [
    # Route pour la mise à jour du profil utilisateur
    path('profile/', views.profile_update, name='profile_update'),
]
