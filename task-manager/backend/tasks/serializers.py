from rest_framework import serializers
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from .models import Task, Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'body', 'created_at']
        read_only_fields = ['author', 'task']


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee', write_only=True,
        required=False, allow_null=True
    )
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'title', 'description', 'status', 'priority',
            'assignee', 'assignee_id', 'created_by', 'due_date', 'order',
            'comments', 'comment_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_by']

    def get_comment_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        request = self.context['request']
        validated_data['created_by'] = request.user
        return super().create(validated_data)


class TaskReorderSerializer(serializers.Serializer):
    """Bulk-update ordering/status after a Kanban drag-and-drop."""
    id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    order = serializers.IntegerField()
