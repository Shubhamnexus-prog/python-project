from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "editor"

urlpatterns = [
    path("login/", views.StyledLoginView.as_view(), name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", LogoutView.as_view(next_page="editor:login"), name="logout"),

    path("", views.document_list, name="document_list"),
    path("new/", views.document_create, name="document_create"),
    path("doc/<int:pk>/", views.document_edit, name="document_edit"),
    path("doc/<int:pk>/autosave/", views.document_autosave, name="document_autosave"),
    path("doc/<int:pk>/favorite/", views.document_toggle_favorite, name="document_toggle_favorite"),
    path("doc/<int:pk>/trash/", views.document_trash, name="document_trash"),
    path("doc/<int:pk>/restore/", views.document_restore, name="document_restore"),
    path("doc/<int:pk>/delete/", views.document_delete_forever, name="document_delete_forever"),
    path("doc/<int:pk>/versions/", views.document_versions, name="document_versions"),
    path("doc/<int:pk>/versions/<int:version_id>/restore/", views.document_version_restore, name="document_version_restore"),
    path("doc/<int:pk>/export/txt/", views.document_export_txt, name="document_export_txt"),
    path("doc/<int:pk>/export/pdf/", views.document_export_pdf, name="document_export_pdf"),

    path("categories/", views.category_manage, name="category_manage"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
]
