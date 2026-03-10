from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User sees projects they created or are members of
        user = self.request.user
        return Project.objects.filter(Q(creator=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User sees tasks in projects they are involved in
        user = self.request.user
        return Task.objects.filter(Q(project__creator=user) | Q(project__members=user)).distinct()

    def perform_create(self, serializer):
        # Additional check if needed, though serializer.validate handles most
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Role-based restriction: Assigned user can only update status
        if instance.project.creator != request.user and instance.assigned_to == request.user:
            allowed_fields = ['status']
            data = {field: request.data.get(field) for field in allowed_fields if field in request.data}
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
            
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Only project creator can delete tasks
        if instance.project.creator != request.user:
            return Response(
                {"detail": "Seul le créateur du projet peut supprimer des tâches."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
