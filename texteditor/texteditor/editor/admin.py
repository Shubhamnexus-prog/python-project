from django.contrib import admin
from .models import Document, Category, Tag, DocumentVersion


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "is_favorite", "is_trashed", "updated_at")
    list_filter = ("is_favorite", "is_trashed", "category")
    search_fields = ("title", "content")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "color")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ("document", "title", "created_at")
