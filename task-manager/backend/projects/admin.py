from django.contrib import admin
from .models import Project, ProjectMembership


class ProjectMembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'task_count', 'created_at')
    search_fields = ('name', 'owner__username')
    inlines = [ProjectMembershipInline]
