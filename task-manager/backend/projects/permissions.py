from rest_framework import permissions


class IsProjectMember(permissions.BasePermission):
    """Only members (or the owner) of a project can view/edit it."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.owner_id == user.id:
            return True
        return obj.members.filter(id=user.id).exists()
