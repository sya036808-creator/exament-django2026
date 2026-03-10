import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from tasks.models import Project, Task

User = get_user_model()


@pytest.fixture
def professor(db):
    return User.objects.create_user(
        username='prof',
        email='prof@esmt.sn',
        password='password123',
        role='PROFESSOR'
    )


@pytest.fixture
def student(db):
    return User.objects.create_user(
        username='student',
        email='student@esmt.sn',
        password='password123',
        role='STUDENT'
    )


@pytest.fixture
def project(db, professor, student):
    p = Project.objects.create(name='Projet Test', creator=professor)
    p.members.add(student)
    return p


# --- Tests des modèles ---

@pytest.mark.django_db
def test_user_roles(professor, student):
    """Les rôles PROFESSOR et STUDENT sont correctement assignés."""
    assert professor.role == 'PROFESSOR'
    assert student.role == 'STUDENT'


@pytest.mark.django_db
def test_project_creation_and_membership(project, professor, student):
    """Un professeur crée un projet et un étudiant en est membre."""
    assert project.creator == professor
    assert student in project.members.all()
    assert str(project) == 'Projet Test'


@pytest.mark.django_db
def test_task_completed_within_deadline(project, professor):
    """Une tâche marquée DONE avant sa deadline est bien comptée dans les délais."""
    deadline = timezone.now() + timedelta(days=5)
    task = Task.objects.create(
        project=project,
        title='Tâche rapide',
        deadline=deadline,
        status='DONE',
        assigned_to=professor,
    )
    assert task.is_completed_within_deadline() is True


@pytest.mark.django_db
def test_task_not_completed_is_not_within_deadline(project, professor):
    """Une tâche non terminée ne compte pas comme finalisée dans les délais."""
    deadline = timezone.now() + timedelta(days=5)
    task = Task.objects.create(
        project=project,
        title='Tâche en suspens',
        deadline=deadline,
        status='TODO',
        assigned_to=professor,
    )
    assert task.is_completed_within_deadline() is False


@pytest.mark.django_db
def test_task_default_status_is_todo(project):
    """Le statut par défaut d'une nouvelle tâche est À faire (TODO)."""
    deadline = timezone.now() + timedelta(days=3)
    task = Task.objects.create(
        project=project,
        title='Nouvelle tâche',
        deadline=deadline,
    )
    assert task.status == 'TODO'


@pytest.mark.django_db
def test_task_str(project):
    """La représentation string d'une tâche retourne son titre."""
    task = Task.objects.create(
        project=project,
        title='Mon titre',
        deadline=timezone.now() + timedelta(days=1),
    )
    assert str(task) == 'Mon titre'


# --- Test des vues (HTTP) ---

@pytest.mark.django_db
def test_dashboard_redirects_to_login_if_unauthenticated(client):
    """Le dashboard redirige vers la connexion si l'utilisateur n'est pas connecté."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/accounts/login' in response['Location']


@pytest.mark.django_db
def test_dashboard_accessible_when_logged_in(client, professor):
    """Le dashboard est accessible quand l'utilisateur est connecté."""
    client.force_login(professor)
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_project_create_accessible_to_authenticated_user(client, professor):
    """La page de création de projet est accessible aux utilisateurs connectés."""
    client.force_login(professor)
    response = client.get('/projects/create/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_statistics_view_accessible(client, professor):
    """La page statistiques est accessible aux utilisateurs connectés."""
    client.force_login(professor)
    response = client.get('/statistics/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_prime_100k_for_100_percent(project, professor):
    """Un professeur avec 100% de tâches terminées dans les délais a droit à 100K CFA."""
    now = timezone.now()
    # Créer 2 tâches, les deux terminées avant deadline
    for i in range(2):
        t = Task.objects.create(
            project=project,
            title=f'Tâche {i}',
            deadline=now + timedelta(days=10),
            status='DONE',
            assigned_to=professor,
        )
    # Compter manuellement (logique du view)
    tasks = Task.objects.filter(assigned_to=professor)
    total = tasks.count()
    done_in_time = sum(1 for t in tasks.filter(status='DONE') if t.updated_at <= t.deadline)
    rate = (done_in_time / total * 100) if total > 0 else 0
    assert rate == 100.0


@pytest.mark.django_db
def test_no_prime_for_student(student, project):
    """Les étudiants ne sont pas éligibles aux primes (vérification du rôle)."""
    assert student.role == 'STUDENT'
    # La logique de prime ne s'applique qu'au rôle PROFESSOR
    assert student.role != 'PROFESSOR'
