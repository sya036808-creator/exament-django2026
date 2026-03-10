from django.contrib.auth.models import AbstractUser
from django.db import models

# Modèle utilisateur personnalisé qui hérite de la classe AbstractUser de Django
class CustomUser(AbstractUser):
    # Définition des choix possibles pour le rôle de l'utilisateur
    ROLE_CHOICES = (
        ('STUDENT', 'Étudiant'),
        ('PROFESSOR', 'Professeur'),
    )
    
    # Champ de rôle pour déterminer si l'utilisateur est un étudiant ou un professeur
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    # Champ d'image de profil (avatar) facultatif pour l'utilisateur
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Méthode pour afficher une représentation lisible de l'utilisateur
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
