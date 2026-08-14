from django.db.models import Q, Count
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project, ProjectMembership
from .serializers import ProjectSerializer, InviteMemberSerializer
from .permissions import IsProjectMember


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        user = self.request.user
        return (
            Project.objects.filter(Q(owner=user) | Q(members=user))
            .distinct()
            .annotate(task_count=Count('tasks', distinct=True))
        )

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def invite(self, request, pk=None):
        project = self.get_object()
        if project.owner_id != request.user.id:
            return Response({'detail': 'Only the owner can invite members.'}, status=403)
        serializer = InviteMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ProjectMembership.objects.get_or_create(
            project=project, user=serializer.user, defaults={'role': 'member'}
        )
        return Response(ProjectSerializer(project, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        project = self.get_object()
        ProjectMembership.objects.filter(project=project, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
