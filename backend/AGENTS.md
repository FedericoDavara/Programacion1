# BACKEND KNOWLEDGE BASE

## OVERVIEW
Flask REST API handling users, workouts ("planificaciones"), classes, and authentication.

## STRUCTURE
```
backend/main/
├── __init__.py       # App factory, DB config, Route registration
├── resources/        # API Resource controllers (GET/POST logic)
├── models/           # SQLAlchemy data models
├── auth/             # Login/Register + JWT protection
├── mail/             # Email sending logic
└── templates/        # Email/HTML templates
```

## KEY PATTERNS
- **Factory Pattern**: App created in `__init__.py:create_app()`.
- **Blueprints**: Auth routes use Blueprint (`auth/routes.py`).
- **RESTful**: endpoints defined as Classes inheriting `Resource`.
- **Config**: Loaded from `.env` via `dotenv` (DB path, Mail config).

## DATABASE
- **ORM**: SQLAlchemy.
- **Migration**: Flask-Migrate (Alembic).
- **URI**: SQLite by default (configured in `create_app`).

## AUTHENTICATION
- **Lib**: `Flask-JWT-Extended`.
- **Flow**: `/auth/login` -> returns Access Token.
- **Protection**: `@jwt_required()` decorator for protected routes.
