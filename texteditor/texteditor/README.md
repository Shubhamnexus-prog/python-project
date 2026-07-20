# Inkwell — Django Text Editor

A full-featured web-based text editor built with Django. Every user has their own private,
autosaving document library with categories, tags, favorites, trash, version history, and
export to PDF/TXT.

## Features

- **Accounts** — sign up, sign in, sign out. Every document is private to its owner.
- **Rich text editing** — bold, italic, underline, headings, bullet/numbered lists, blockquotes,
  text alignment, undo/redo. Keyboard shortcuts: `Ctrl/Cmd+B/I/U`, `Ctrl/Cmd+S`.
- **Autosave** — saves ~1 second after you stop typing, plus a save-on-exit beacon so you never
  lose work. Live "Saved at ..." status and a live word/character count.
- **Version history** — automatic snapshots are kept as you edit (every save with meaningful
  changes, plus a snapshot every 2 minutes of active editing). Browse and restore any past
  version; restoring snapshots your current draft first, so nothing is ever truly lost.
- **Organization** — custom color-coded categories and free-form comma-separated tags.
- **Search & filters** — full-text search across title and content, plus filter by category, tag,
  favorites, or trash.
- **Favorites & trash** — star important documents; soft-delete with a trash view, restore, or
  permanently delete.
- **Export** — download any document as a plain `.txt` file or a formatted `.pdf`.
- **Dark mode** — toggle in the sidebar, remembered across visits.
- **Admin panel** — manage everything from Django's built-in `/admin/` too.

## Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up the database
python manage.py migrate

# 4. Create your own account (or use the signup page once running)
python manage.py createsuperuser

# 5. Run the dev server
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** — you'll land on the login page. Click "Create an account"
to sign up, or sign in if you already made one with `createsuperuser`.

## Project structure

```
texteditor_project/     # Django project settings & root URLs
editor/                 # The app: models, views, forms, templates, static assets
  models.py              # Document, Category, Tag, DocumentVersion
  views.py                # All page + JSON autosave/API views
  urls.py                 # editor: namespaced routes
  templates/editor/       # HTML templates (base, dashboard, editor, versions, categories, auth)
  static/editor/           # main.css (design system) + main.js (theme toggle)
manage.py
requirements.txt
```

## Notes on extending it

- **Rich text storage**: content is stored as sanitized-by-the-browser HTML from a
  `contenteditable` surface. If you expose this publicly, add server-side HTML sanitization
  (e.g. `bleach`) before trusting `doc.content` in templates.
- **Autosave endpoint**: `POST /doc/<id>/autosave/` accepts JSON
  `{title, content, category_id, tags, snapshot}` and returns the new word/char counts.
- **PDF export** uses `reportlab` directly (no external binaries needed).
- To add collaborators/sharing, you'd extend `Document` with a many-to-many "shared_with" field
  and adjust the `_owned_document_or_404` check in `views.py`.
