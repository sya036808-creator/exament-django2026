# Rapport de Projet - Gestion des Tâches Collaboratives

## Présentation du Projet
Ce projet a été réalisé dans le cadre de l'examen Django pour l'ESMT. L'objectif est de créer une application web permettant de gérer des projets et des tâches en équipe, avec un suivi particulier pour les enseignants (professeurs) et les étudiants.

## Fonctionnalités principales
- **Espace Membre** : Chaque utilisateur (étudiant ou prof) peut s'inscrire et se connecter.
- **Gestion des Projets** : On peut créer un projet, ajouter une description et choisir les membres qui participent.
- **Tâches et Suivi** : Dans chaque projet, le créateur peut ajouter des tâches. Les membres assignés peuvent ensuite changer le statut (En cours, Terminé).
- **Calcul des Primes** : Le système calcule automatiquement si un professeur a droit à une prime (30 000 ou 100 000 CFA) selon s'il finit ses tâches à temps durant l'année.

## Choix techniques
- **Django** : Framework principal pour la rapidité et la sécurité.
- **Bootstrap** : Pour avoir une interface propre et responsive sur mobile.
- **CSS Personnalisé** : J'ai ajouté quelques styles pour rendre l'interface plus moderne.
- **Permissions** : J'ai mis en place des règles pour que les étudiants ne puissent pas donner d'ordres (tâches) aux professeurs.

## Lancement
Pour faire tourner le projet :
1. Activer l'environnement venv.
2. Installer les requirements (`pip install -r requirements.txt`).
3. Faire les migrations et lancer le serveur.

Réalisé par : ALPHA SY
ESMT 2026
