from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Project, ProjectMembership

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    task_count = serializers.IntegerField(read_only=True)
    done_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'color', 'owner', 'members',
            'task_count', 'done_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['owner']

    def create(self, validated_data):
        request = self.context['request']
        project = Project.objects.create(owner=request.user, **validated_data)
        ProjectMembership.objects.create(project=project, user=request.user, role='owner')
        return project


class InviteMemberSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user with that username exists.')
        self.user = user
        return value
