import io
import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Document, Category, Tag, DocumentVersion
from .forms import SignUpForm, DocumentMetaForm, CategoryForm


# ---------- Auth ----------

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("editor:document_list")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("editor:document_list")
    else:
        form = SignUpForm()
    return render(request, "editor/signup.html", {"form": form})


class StyledLoginView(LoginView):
    template_name = "editor/login.html"


# ---------- Helpers ----------

def _owned_document_or_404(request, pk):
    return get_object_or_404(Document, pk=pk, owner=request.user)


def _parse_tags(raw, owner):
    names = [t.strip() for t in raw.split(",") if t.strip()]
    tags = []
    for name in names:
        tag, _ = Tag.objects.get_or_create(owner=owner, name=name)
        tags.append(tag)
    return tags


# ---------- Document list / dashboard ----------

@login_required
def document_list(request):
    q = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    tag_id = request.GET.get("tag", "")
    filter_mode = request.GET.get("filter", "")  # favorites / trash

    docs = Document.objects.filter(owner=request.user)

    if filter_mode == "trash":
        docs = docs.filter(is_trashed=True)
    else:
        docs = docs.filter(is_trashed=False)
        if filter_mode == "favorites":
            docs = docs.filter(is_favorite=True)

    if q:
        docs = docs.filter(Q(title__icontains=q) | Q(content__icontains=q))

    if category_id:
        docs = docs.filter(category_id=category_id)

    if tag_id:
        docs = docs.filter(tags__id=tag_id)

    docs = docs.distinct()

    paginator = Paginator(docs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    categories = Category.objects.filter(owner=request.user)
    tags = Tag.objects.filter(owner=request.user)

    return render(request, "editor/document_list.html", {
        "page_obj": page_obj,
        "categories": categories,
        "tags": tags,
        "q": q,
        "selected_category": category_id,
        "selected_tag": tag_id,
        "filter_mode": filter_mode,
    })


@login_required
@require_POST
def document_create(request):
    doc = Document.objects.create(owner=request.user, title="Untitled Document", content="")
    return redirect("editor:document_edit", pk=doc.pk)


@login_required
def document_edit(request, pk):
    doc = _owned_document_or_404(request, pk)
    meta_form = DocumentMetaForm(owner=request.user, instance=doc)
    categories = Category.objects.filter(owner=request.user)
    tag_names = ", ".join(doc.tags.values_list("name", flat=True))
    return render(request, "editor/editor.html", {
        "doc": doc,
        "meta_form": meta_form,
        "categories": categories,
        "tag_names": tag_names,
    })


@login_required
@require_POST
def document_autosave(request, pk):
    doc = _owned_document_or_404(request, pk)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "bad payload"}, status=400)

    title = payload.get("title", doc.title).strip() or "Untitled Document"
    content = payload.get("content", doc.content)
    category_id = payload.get("category_id")
    raw_tags = payload.get("tags", "")
    take_snapshot = payload.get("snapshot", False)

    content_changed = content != doc.content
    doc.title = title
    doc.content = content
    doc.category_id = category_id or None
    doc.save()

    if raw_tags is not None:
        tags = _parse_tags(raw_tags, request.user)
        doc.tags.set(tags)

    if take_snapshot and content_changed:
        doc.make_version_snapshot()

    return JsonResponse({
        "ok": True,
        "updated_at": timezone.localtime(doc.updated_at).strftime("%b %d, %Y %I:%M %p"),
        "word_count": doc.word_count,
        "char_count": doc.char_count,
    })


@login_required
@require_POST
def document_toggle_favorite(request, pk):
    doc = _owned_document_or_404(request, pk)
    doc.is_favorite = not doc.is_favorite
    doc.save(update_fields=["is_favorite"])
    return JsonResponse({"ok": True, "is_favorite": doc.is_favorite})


@login_required
@require_POST
def document_trash(request, pk):
    doc = _owned_document_or_404(request, pk)
    doc.is_trashed = True
    doc.save(update_fields=["is_trashed"])
    messages.success(request, f'"{doc.title}" moved to trash.')
    return redirect("editor:document_list")


@login_required
@require_POST
def document_restore(request, pk):
    doc = _owned_document_or_404(request, pk)
    doc.is_trashed = False
    doc.save(update_fields=["is_trashed"])
    messages.success(request, f'"{doc.title}" restored.')
    return redirect("editor:document_list")


@login_required
@require_POST
def document_delete_forever(request, pk):
    doc = _owned_document_or_404(request, pk)
    title = doc.title
    doc.delete()
    messages.success(request, f'"{title}" permanently deleted.')
    return redirect("editor:document_list")


@login_required
def document_versions(request, pk):
    doc = _owned_document_or_404(request, pk)
    versions = doc.versions.all()
    return render(request, "editor/versions.html", {"doc": doc, "versions": versions})


@login_required
@require_POST
def document_version_restore(request, pk, version_id):
    doc = _owned_document_or_404(request, pk)
    version = get_object_or_404(DocumentVersion, pk=version_id, document=doc)
    doc.make_version_snapshot()  # snapshot current state before overwrite
    doc.title = version.title
    doc.content = version.content
    doc.save()
    messages.success(request, "Version restored.")
    return redirect("editor:document_edit", pk=doc.pk)


# ---------- Export ----------

@login_required
def document_export_txt(request, pk):
    import re
    doc = _owned_document_or_404(request, pk)
    text = re.sub("<[^>]+>", "", doc.content or "")
    response = HttpResponse(text, content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{doc.title}.txt"'
    return response


@login_required
def document_export_pdf(request, pk):
    import re
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import simpleSplit

    doc = _owned_document_or_404(request, pk)
    text = re.sub("<[^>]+>", "", doc.content or "")

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 0.85 * inch
    max_width = width - 2 * margin

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, height - margin, doc.title)

    c.setFont("Helvetica", 11)
    y = height - margin - 0.4 * inch
    line_height = 15

    for paragraph in text.split("\n"):
        lines = simpleSplit(paragraph, "Helvetica", 11, max_width) or [""]
        for line in lines:
            if y < margin:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - margin
            c.drawString(margin, y, line)
            y -= line_height

    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{doc.title}.pdf"'
    return response


# ---------- Categories ----------

@login_required
def category_manage(request):
    categories = Category.objects.filter(owner=request.user)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.owner = request.user
            cat.save()
            messages.success(request, f'Category "{cat.name}" created.')
            return redirect("editor:category_manage")
    else:
        form = CategoryForm()
    return render(request, "editor/categories.html", {"categories": categories, "form": form})


@login_required
@require_POST
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk, owner=request.user)
    cat.delete()
    messages.success(request, "Category deleted.")
    return redirect("editor:category_manage")
