import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from tasks.models import Project, Task

User = get_user_model()

@pytest.fixture
def create_test_users(db):
    prof = User.objects.create_user(username='prof1', email='prof1@esmt.sn', password='pwd', role='PROFESSOR')
    student = User.objects.create_user(username='student1', email='student1@esmt.sn', password='pwd', role='STUDENT')
    return prof, student

@pytest.fixture
def create_test_project(create_test_users):
    prof, _ = create_test_users
    return Project.objects.create(
        name="Projet de Test",
        description="Une description de test",
        creator=prof
    )

@pytest.mark.django_db
class TestProjectModel:
    def test_create_project(self, create_test_project):
        project = create_test_project
        assert project.name == "Projet de Test"
        assert project.description == "Une description de test"
        assert project.creator.username == "prof1"
        assert str(project) == "Projet de Test"

@pytest.mark.django_db
class TestTaskModel:
    def test_create_task(self, create_test_project, create_test_users):
        project = create_test_project
        prof, student = create_test_users
        
        task = Task.objects.create(
            title="Tâche 1",
            description="Faire le backend",
            project=project,
            assigned_to=student,
            status='TODO',
            deadline=timezone.now() + timedelta(days=2)
        )
        
        assert task.title == "Tâche 1"
        assert task.project == project
        assert task.assigned_to == student
        assert task.status == 'TODO'
        assert str(task) == "Tâche 1"
