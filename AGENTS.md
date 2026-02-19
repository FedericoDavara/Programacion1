# PROJECT KNOWLEDGE BASE

**Generated:** 2026-02-19
**Context:** GOL GYM (Full Stack App)

## OVERVIEW
GOL GYM is a gym management system with user/role management, workout planning, and class scheduling.
**Stack:** Angular 16 (Frontend) + Flask/Python 3 (Backend) + SQLite/SQLAlchemy.

## STRUCTURE
```
.
├── backend/                  # Python Flask API
│   ├── main/                 # Application source
│   │   ├── resources/        # API Endpoints (Flask-RESTful)
│   │   ├── models/           # Database Models
│   │   ├── auth/             # JWT Authentication
│   │   └── mail/             # Email notifications
│   ├── migrations/           # Alembic/Flask-Migrate versions
│   └── requirements.txt      # Python dependencies
└── frontend/
    └── gol_gym/              # Angular Project Root
        ├── src/app/          # Components, Services, Pages
        └── package.json      # NPM dependencies
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **API Routes** | `backend/main/resources/` | mapped in `backend/main/__init__.py` |
| **DB Models** | `backend/main/models/` | SQLAlchemy entities |
| **Auth Logic** | `backend/main/auth/` | JWT handling & decorators |
| **Pages** | `frontend/.../src/app/pages/` | Angular views (Login, Home, Perfil) |
| **Components** | `frontend/.../src/app/components/` | Reusable UI (Navbar, Forms) |
| **Services** | `frontend/.../src/app/services/` | HTTP calls to Backend |

## CONVENTIONS
- **Backend:** Flask Application Factory pattern (`create_app`).
- **API:** RESTful design using `flask_restful` Resources.
- **Frontend:** Angular Modules pattern (`app.module.ts` declares all).
- **Styling:** CSS/SASS with Bootstrap icons.

## COMMANDS
```bash
# Backend
cd backend && bash boot.sh        # Start API
cd backend && bash install.sh     # Install deps

# Frontend
cd frontend/gol_gym && ng serve -o  # Dev server (port 4200)
cd frontend/gol_gym && ng test      # Run unit tests
```
