# ESMT Task Manager — Application de Gestion des Tâches Collaboratives

Application web Django pour la gestion collaborative des tâches à l'ESMT, avec deux profils utilisateurs (Étudiant / Professeur), gestion de projets, suivi des tâches, statistiques et système de primes.

---

## 1. Documentation et Lancement du Projet (Livrable 2.a)

### Prérequis
- Python 3.10+
- pip
- Git

### Instructions d'installation et de lancement

```bash
# 1. Cloner le dépôt (si depuis GitHub/GitLab)
git clone https://github.com/TON_USERNAME/esmt-task-manager.git
cd esmt-task-manager

# 2. Créer et activer l'environnement virtuel
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Installer les dépendances (Django, DRF, Allauth, Pytest, etc.)
pip install -r requirements.txt

# 4. Appliquer les migrations de base de données
python manage.py makemigrations
python manage.py migrate

# 5. Créer un superutilisateur (Administrateur global)
python manage.py createsuperuser

# 6. Lancer le serveur de développement
python manage.py runserver
```

L'application web est accessible sur **http://127.0.0.1:8000/**

### Lancement des Tests Unitaires (Pytest)

Le projet intègre `pytest-django` pour valider les fonctionnalités principales (création d'utilisateurs avec rôles, création de projets, et création de tâches).

Pour lancer la suite de tests, exécutez simplement :
```bash
pytest -v
```

---

## 2. Explication des Modèles de Données (Livrable 2.b)

L'application repose sur 3 modèles principaux interconnectés :

### 1. CustomUser (`users/models.py`)
Ce modèle étend le modèle utilisateur par défaut de Django (`AbstractUser`) pour ajouter les rôles spécifiques au projet ESMT.

- **`username`**, **`email`**, **`password`** : Champs standards d'authentification.
- **`role`** : Choix entre `STUDENT` (Étudiant) et `PROFESSOR` (Professeur). Ce rôle détermine les droits dans l'application (un prof peut assigner, un étudiant ne peut que consulter et mettre à jour le statut).
- **`phone_number`** : Numéro de téléphone pour la réception des SMS de réinitialisation de mot de passe.
- **`avatar`** : Photo de profil de l'utilisateur.

### 2. Project (`tasks/models.py`)
Représente un projet de groupe collaboratif.

- **`name`** : Nom du projet.
- **`description`** : Détails du projet.
- **`creator`** : `ForeignKey` vers `CustomUser`. L'utilisateur (généralement un Professeur) qui a créé le projet.
- **`members`** : `ManyToManyField` vers `CustomUser`. Les étudiants/professeurs assignés à ce projet.

### 3. Task (`tasks/models.py`)
Représente une tâche spécifique au sein d'un projet.

- **`project`** : `ForeignKey` vers `Project`. Le projet auquel cette tâche appartient (relation 1-N).
- **`title`** & **`description`** : Détails de la tâche.
- **`deadline`** : Date et heure limite d'exécution. Moteur de calcul pour les statistiques de livraison à temps.
- **`status`** : Son état d'avancement (`TODO`, `IN_PROGRESS`, `DONE`).
- **`assigned_to`** : `ForeignKey` vers `CustomUser`. L'utilisateur chargé de réaliser cette tâche.

---

## 3. Routes API Disponibles (Livrable 2.b)

Le projet expose une **API RESTful** développée avec Django REST Framework pour permettre à d'autres applications (Mobile, Front-end JS) de se connecter.

La documentation interactive complète (Swagger UI) est disponible à l'adresse : **[http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)**

### Endpoints Principaux

| Endpoint API REST | Méthode HTTP | Description |
|-------------------|--------------|-------------|
| `/api/projects/` | `GET`, `POST` | Récupérer la liste des projets ou en créer un nouveau |
| `/api/projects/<id>/` | `GET`, `PUT`, `DELETE` | Lire, modifier ou supprimer un projet spécifique |
| `/api/tasks/` | `GET`, `POST` | Récupérer la liste des tâches ou assigner une nouvelle tâche |
| `/api/tasks/<id>/` | `GET`, `PUT`, `DELETE` | Lire, modifier ou supprimer une tâche spécifique |

### Authentification de l'API (JWT)

| Endpoint | Méthode HTTP | Description |
|----------|--------------|-------------|
| `/api/token/` | `POST` | Envoyer ses identifiants pour obtenir un Token d'Accès et de Rafraîchissement JWT |
| `/api/token/refresh/` | `POST` | Obtenir un nouveau token d'accès avant l'expiration du précédent |

