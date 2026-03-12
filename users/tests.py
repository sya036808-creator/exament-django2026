import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    def test_create_student_user(self):
        user = User.objects.create_user(
            username='etudiant1',
            email='etudiant1@esmt.sn',
            password='password123',
            role='STUDENT',
            phone_number='771234567'
        )
        assert user.username == 'etudiant1'
        assert user.email == 'etudiant1@esmt.sn'
        assert user.role == 'STUDENT'
        assert user.phone_number == '771234567'
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_professor_user(self):
        user = User.objects.create_user(
            username='prof1',
            email='prof1@esmt.sn',
            password='password123',
            role='PROFESSOR'
        )
        assert user.username == 'prof1'
        assert user.role == 'PROFESSOR'
        assert user.is_active is True

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@esmt.sn',
            password='superuserpassword'
        )
        assert admin_user.username == 'admin'
        assert admin_user.is_active is True
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True
