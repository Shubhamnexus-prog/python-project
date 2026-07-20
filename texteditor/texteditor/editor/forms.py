from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Document, Category


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class DocumentMetaForm(forms.ModelForm):
    """Used for the create dialog and the sidebar meta editing (title/category)."""
    new_tags = forms.CharField(
        required=False,
        help_text="Comma-separated tags",
        widget=forms.TextInput(attrs={"placeholder": "work, ideas, draft"}),
    )

    class Meta:
        model = Document
        fields = ["title", "category"]

    def __init__(self, *args, owner=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner
        if owner is not None:
            self.fields["category"].queryset = Category.objects.filter(owner=owner)
        self.fields["category"].required = False


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "color"]
        widgets = {"color": forms.TextInput(attrs={"type": "color"})}
