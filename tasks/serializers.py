from rest_framework import serializers
from .models import Project, Task
from users.serializers import UserPublicSerializer

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserPublicSerializer(source='assigned_to', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'project', 'title', 'description', 
            'deadline', 'status', 'assigned_to', 'assigned_to_detail',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Custom validation: Students cannot assign Professors
        """
        request = self.context.get('request')
        if request and request.user.role == 'STUDENT':
            assigned_user = data.get('assigned_to')
            if assigned_user and assigned_user.role == 'PROFESSOR':
                raise serializers.ValidationError(
                    {"assigned_to": "Un étudiant ne peut pas assigner un professeur à une tâche."}
                )
        return data

class ProjectSerializer(serializers.ModelSerializer):
    creator_detail = UserPublicSerializer(source='creator', read_only=True)
    members_detail = UserPublicSerializer(source='members', many=True, read_only=True)
    tasks_count = serializers.IntegerField(source='tasks.count', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'creator', 'creator_detail',
            'members', 'members_detail', 'tasks_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']
