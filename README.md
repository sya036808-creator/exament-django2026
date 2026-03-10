# ESMT Task Manager — Application de Gestion des Tâches Collaboratives

Application web Django pour la gestion collaborative des tâches à l'ESMT, avec deux profils utilisateurs (Étudiant / Professeur), gestion de projets, suivi des tâches, statistiques et système de primes.

---

## 1. Configuration et Lancement du Projet

### Prérequis
- Python 3.10+
- pip

### Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/TON_USERNAME/esmt-task-manager.git
cd esmt-task-manager

# 2. Créer et activer l'environnement virtuel
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un superutilisateur (admin)
python manage.py createsuperuser

# 6. Lancer le serveur de développement
python manage.py runserver
```

L'application est accessible sur **http://127.0.0.1:8000/**

### Comptes de démonstration

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Administrateur | admin@esmt.sn | Jacke120@ |
| Professeur | prof@esmt.sn | Jacke120@ |

---

## 2. Modèles de Données

### CustomUser (`users/models.py`)
Extension du modèle Django `AbstractUser`.

| Champ | Type | Description |
|-------|------|-------------|
| `username` | CharField | Nom d'utilisateur unique |
| `email` | EmailField | Adresse email (utilisée pour la connexion) |
| `role` | CharField | `STUDENT` (Étudiant) ou `PROFESSOR` (Professeur) |
| `avatar` | ImageField | Photo de profil (optionnel) |

### Project (`tasks/models.py`)

| Champ | Type | Description |
|-------|------|-------------|
| `name` | CharField | Nom du projet |
| `description` | TextField | Description détaillée |
| `creator` | ForeignKey → User | Créateur du projet |
| `members` | ManyToManyField → User | Membres de l'équipe |
| `created_at` | DateTimeField | Date de création |

### Task (`tasks/models.py`)

| Champ | Type | Description |
|-------|------|-------------|
| `project` | ForeignKey → Project | Projet parent |
| `title` | CharField | Titre de la tâche |
| `description` | TextField | Description |
| `deadline` | DateTimeField | Date limite d'exécution |
| `status` | CharField | `TODO`, `IN_PROGRESS`, ou `DONE` |
| `assigned_to` | ForeignKey → User | Utilisateur assigné |

---

## 3. Routes de l'Application

### Application Web (Templates Django)

| URL | Description |
|-----|-------------|
| `/` | Tableau de bord avec filtres |
| `/projects/` | Liste des projets |
| `/projects/create/` | Créer un projet |
| `/projects/<id>/` | Détails d'un projet et ses tâches |
| `/projects/<id>/update/` | Modifier un projet |
| `/projects/<id>/delete/` | Supprimer un projet |
| `/projects/<id>/tasks/create/` | Créer une tâche |
| `/tasks/<id>/update/` | Modifier une tâche |
| `/tasks/<id>/delete/` | Supprimer une tâche |
| `/statistics/` | Statistiques et primes |
| `/accounts/login/` | Connexion |
| `/accounts/signup/` | Inscription |

### API REST

Documentation interactive : **http://127.0.0.1:8000/api/docs/**

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/projects/` | GET, POST | Liste et création de projets |
| `/api/projects/<id>/` | GET, PUT, DELETE | Gestion d'un projet |
| `/api/tasks/` | GET, POST | Liste et création de tâches |
| `/api/tasks/<id>/` | GET, PUT, DELETE | Gestion d'une tâche |
| `/api/token/` | POST | Obtenir un token JWT |
| `/api/token/refresh/` | POST | Rafraîchir le token JWT |

---

## 4. Fonctionnalités

- Authentification par email (connexion / inscription)
- Deux profils : Étudiant et Professeur
- Création et gestion de projets collaboratifs
- Gestion des tâches avec statuts (À faire / En cours / Terminé)
- Filtrage des tâches par statut et par membre
- Statistiques trimestrielles et annuelles
- Calcul automatique des primes (30 000 CFA à 90% · 100 000 CFA à 100%)
- API REST avec authentification JWT

---

## 5. Technologies

| Technologie | Usage |
|-------------|-------|
| Python 3.14 / Django 6.0 | Backend |
| Django REST Framework | API REST |
| django-allauth | Authentification |
| djangorestframework-simplejwt | Tokens JWT |
| Bootstrap 5.3 | Interface utilisateur |
| SQLite | Base de données |

---

## 6. Structure du Projet

```
esmt-task-manager/
├── esmt_task_manager/     # Configuration Django
├── tasks/                 # Projets et tâches
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── api_views.py
├── users/                 # Gestion des utilisateurs
│   ├── models.py
│   └── forms.py
├── templates/             # Templates HTML
├── static/                # CSS, images
└── manage.py
```
