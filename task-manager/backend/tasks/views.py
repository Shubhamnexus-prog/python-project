from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from projects.models import Project
from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer, TaskReorderSerializer


class IsTaskProjectMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj.project if hasattr(obj, 'project') else obj.task.project
        user = request.user
        return project.owner_id == user.id or project.members.filter(id=user.id).exists()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskProjectMember]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'status', 'priority', 'assignee']

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(project__owner=user) | Q(project__members=user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if not (project.owner_id == self.request.user.id or
                project.members.filter(id=self.request.user.id).exists()):
            raise permissions.PermissionDenied('Not a member of this project.')
        serializer.save()

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """Accepts a list of {id, status, order} after a drag-and-drop move
        on the Kanban board and persists the new positions in one transaction."""
        serializer = TaskReorderSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        task_ids = [item['id'] for item in serializer.validated_data]
        tasks = {t.id: t for t in self.get_queryset().filter(id__in=task_ids)}

        with transaction.atomic():
            for item in serializer.validated_data:
                task = tasks.get(item['id'])
                if task is None:
                    continue
                task.status = item['status']
                task.order = item['order']
                task.save(update_fields=['status', 'order'])

        return Response({'updated': len(tasks)})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskProjectMember]

    def get_queryset(self):
        user = self.request.user
        qs = Comment.objects.filter(
            Q(task__project__owner=user) | Q(task__project__members=user)
        ).distinct()
        task_id = self.request.query_params.get('task')
        if task_id:
            qs = qs.filter(task_id=task_id)
        return qs

    def perform_create(self, serializer):
        task_id = self.request.data.get('task')
        task = Task.objects.get(id=task_id)
        self.check_object_permissions(self.request, task)
        serializer.save(author=self.request.user, task=task)
