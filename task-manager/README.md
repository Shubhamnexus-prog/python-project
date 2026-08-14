# TaskFlow — Task & Project Management Platform

A full-stack task and project management app: JWT-authenticated multi-user
workspace, projects with team members, and a drag-and-drop Kanban board with
comments — built on a real relational database (no mock/seed JSON).

**Stack:** Django REST Framework · PostgreSQL/SQLite · React (Vite) · Tailwind CSS · JWT auth

---

## Why this project is portfolio-ready

- **Real backend, real database.** Django models + migrations create actual
  tables (`User`, `Project`, `ProjectMembership`, `Task`, `Comment`). Every
  API response comes from the ORM — nothing is hardcoded or generated.
- **Proper auth.** Custom user model, JWT access/refresh tokens
  (`djangorestframework-simplejwt`), automatic token refresh on the frontend.
- **Real permissions.** Only a project's owner/members can view or edit it —
  enforced server-side, not just hidden in the UI.
- **A genuinely interactive feature.** The Kanban board supports drag-and-drop
  across columns, and persists the new status/order to the database via a
  dedicated `/api/tasks/reorder/` endpoint (optimistic UI + server sync).
- **Distinctive UI**, not a default template — a "blueprint / drafting board"
  visual identity (grid backdrop, corner crosshair marks, mono-spaced spec
  labels) that fits a planning tool conceptually.

---

## Project structure

```
TaskFlow/
├── backend/                 # Django REST API
│   ├── taskflow/            # settings, root urls
│   ├── accounts/            # custom User model, register/login/me
│   ├── projects/            # Project + membership, invite/leave
│   ├── tasks/                # Task + Comment, Kanban reorder endpoint
│   └── requirements.txt
└── frontend/                 # React + Vite + Tailwind
    └── src/
        ├── api/axios.js       # API client with auto token refresh
        ├── context/AuthContext.jsx
        ├── pages/             # Login, Register, Dashboard, ProjectBoard
        └── components/        # Navbar, TaskCard, TaskModal, etc.
```

---

## Backend setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate        # creates the real SQLite DB + tables
python manage.py createsuperuser   # optional: for /admin access

python manage.py runserver      # http://localhost:8000
```

The API is served under `/api/`. Django admin is at `/admin/`.

### Switching to PostgreSQL

The models and migrations are Postgres-compatible as-is. In
`backend/taskflow/settings.py`, replace the `DATABASES` block with:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskflow',
        'USER': 'taskflow_user',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
then run `pip install psycopg2-binary` and `python manage.py migrate` again.

### Key API endpoints

| Method | Endpoint                       | Purpose                          |
|--------|---------------------------------|-----------------------------------|
| POST   | `/api/auth/register/`           | Create account, returns JWT pair  |
| POST   | `/api/auth/login/`              | Login, returns JWT pair           |
| POST   | `/api/auth/login/refresh/`      | Refresh access token              |
| GET    | `/api/auth/me/`                 | Current user profile              |
| GET/POST | `/api/projects/`              | List / create projects            |
| POST   | `/api/projects/{id}/invite/`    | Invite a teammate by username     |
| GET/POST | `/api/tasks/?project={id}`    | List / create tasks               |
| PATCH/DELETE | `/api/tasks/{id}/`         | Update / delete a task            |
| POST   | `/api/tasks/reorder/`           | Persist Kanban drag-and-drop order|
| GET/POST | `/api/tasks/comments/`        | List / add comments on a task     |

---

## Frontend setup

```bash
cd frontend
npm install
cp .env.example .env      # points VITE_API_URL at your backend
npm run dev                # http://localhost:5173
```

`npm run build` produces a production bundle in `frontend/dist/`.

---

## Trying it out

1. Start the backend (`python manage.py runserver`) and frontend (`npm run dev`).
2. Open `http://localhost:5173`, register an account.
3. Create a project, add a few tasks, drag them across the Kanban columns.
4. Invite a second account (register another user, then invite by username)
   to see multi-user membership and assignment in action.

---

## Notes for extending it

- Swap SQLite for PostgreSQL in production (see above) — no code changes needed.
- Add WebSockets (Django Channels) for live board updates across users.
- Add file attachments on tasks via `django-storages` + S3.
- Deploy backend to Render/Railway/Fly.io and frontend to Vercel/Netlify;
  set `VITE_API_URL` and `CORS_ALLOWED_ORIGINS` accordingly.
