from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    color = models.CharField(max_length=7, default="#6366f1")

    class Meta:
        unique_together = ("name", "owner")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")

    class Meta:
        unique_together = ("name", "owner")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255, default="Untitled Document")
    content = models.TextField(blank=True, default="")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="documents"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="documents")
    is_favorite = models.BooleanField(default=False)
    is_trashed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("editor:document_edit", args=[self.pk])

    @property
    def word_count(self):
        import re
        text = re.sub("<[^>]+>", " ", self.content or "")
        words = text.split()
        return len(words)

    @property
    def char_count(self):
        import re
        text = re.sub("<[^>]+>", "", self.content or "")
        return len(text)

    def make_version_snapshot(self):
        DocumentVersion.objects.create(
            document=self,
            title=self.title,
            content=self.content,
        )
        old_ids = list(
            self.versions.order_by("-created_at").values_list("id", flat=True)[30:]
        )
        if old_ids:
            DocumentVersion.objects.filter(id__in=old_ids).delete()


class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="versions")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.document.title} @ {self.created_at:%Y-%m-%d %H:%M}"
