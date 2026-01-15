# AGENTS.md - Developer Guide for Agentic Coding Agents

This document serves as the primary source of truth for AI agents operating within this repository. 
It outlines the project structure, build/test commands, and code style conventions.

## 1. Project Structure

This is a full-stack web application consisting of:
- **Backend:** A Flask (Python) REST API located in `backend/`.
- **Frontend:** An Angular 16 application located in `frontend/gol_gym/`.

### Directory Layout
- `/backend`:
  - `app.py`: Application entry point.
  - `main/`: Core application logic (Blueprints).
    - `models/`: SQLAlchemy database models.
    - `resources/`: Flask-RESTful resources.
    - `auth/`: Authentication logic.
    - `mail/`: Email functionality.
  - `requirements.txt`: Python dependencies.
- `/frontend/gol_gym`:
  - `src/`: Angular source code.
  - `package.json`: NPM dependencies and scripts.

## 2. Environment & Commands

### Backend (Python/Flask)
*Note: Ensure the Python virtual environment is activated before running commands.*

**Setup:**
```bash
# Install dependencies
pip install -r backend/requirements.txt
```

**Run Application:**
```bash
# Run the Flask server
python3 backend/app.py
```
*The server typically runs on port defined in environment variables (default 5000).*

**Testing:**
*Currently, there is no established testing framework (like pytest) configured for the backend.*
- **Action:** If tasked with writing backend tests, propose installing `pytest` and creating a `tests/` directory in `backend/`.
- **Legacy:** Do NOT rely on tests found in `site-packages`.

**Linting/Formatting:**
- Follow PEP 8 guidelines.
- Use `flake8` or `black` if available, otherwise mimic existing indentation (4 spaces).

### Frontend (Angular)
*Working Directory: `frontend/gol_gym`*

**Setup:**
```bash
cd frontend/gol_gym
npm install
```

**Run Application:**
```bash
ng serve
# Navigate to http://localhost:4200/
```

**Testing:**
```bash
# Run unit tests (Karma/Jasmine)
ng test

# Run a specific test file (via grep pattern not directly supported by standard ng test, usually requires fit/fdescribe)
# Agent Instruction: To run a single test, modify the spec file to use 'fdescribe' or 'fit' temporarily.
```

**Build:**
```bash
ng build
```

## 3. Code Style & Conventions

### General
- **Indentation:** Use 4 spaces for Python. Use 2 spaces for TypeScript/HTML/CSS.
- **Line Endings:** Unix-style (`\n`).
- **File Encoding:** UTF-8.

### Python (Backend)
- **Framework:** Flask with `Flask-RESTful`, `Flask-SQLAlchemy`, `Flask-JWT-Extended`.
- **Naming Conventions:**
  - Classes: `PascalCase` (e.g., `Usuario`, `Clase`).
  - Variables/Functions: `snake_case` (e.g., `create_app`, `validate_password`).
  - Constants: `UPPER_CASE`.
- **Models (`backend/main/models`):**
  - Inherit from `db.Model`.
  - Use SQLAlchemy `@validates` decorators for field validation.
  - Implement `to_json`, `to_json_short`, and `to_json_complete` methods for serialization. Do not use external serialization libraries unless requested.
  - Example Validation:
    ```python
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email required")
        return email
    ```
- **Resources (`backend/main/resources`):**
  - Inherit from `flask_restful.Resource`.
  - Use `request.get_json()` for input.
  - Return dictionaries that are automatically JSONified.
- **Imports:**
  - Group standard library imports first, then third-party, then local.
  - Use relative imports for local modules where appropriate (e.g., `from .. import db`).

### TypeScript (Frontend)
- **Framework:** Angular 16.
- **Strictness:** Strict mode is likely enabled in `tsconfig.json`. Ensure types are defined.
- **Naming:**
  - Classes/Components: `PascalCase` (e.g., `LoginComponent`).
  - Files: `kebab-case` (e.g., `login.component.ts`).
  - Methods/Variables: `camelCase`.
- **Observables:** Use `$` suffix for variables holding Observables (e.g., `user$`).
- **Structure:**
  - Components should implement `OnInit`, `OnDestroy` if needed.
  - Use dependency injection via constructor.

## 4. Error Handling

- **Backend:**
  - Raise `ValueError` in models for validation failures.
  - Catch exceptions in Resources and return appropriate HTTP status codes (400 for bad request, 404 for not found, 500 for server error).
  - Use `try/except` blocks for database operations.

- **Frontend:**
  - Handle Observable errors using `.pipe(catchError(...))`.
  - Display user-friendly error messages in the UI.

## 5. Agent Operational Rules

1.  **File Paths:** ALWAYS use absolute paths when reading/writing files.
    - Example: `/home/adriano/Dev/Facultad/Programacion1/backend/app.py`
2.  **Safety First:**
    - Read files before editing to understand context.
    - If unsure about a dependency, check `requirements.txt` or `package.json` first.
3.  **No Hallucinations:**
    - Do not invent build commands. Use the ones listed above.
    - Do not reference non-existent tests.
4.  **Refactoring:**
    - When modifying models, ensure `to_json` methods are updated to reflect schema changes.
    - When modifying API endpoints, check if frontend services need updates.

## 6. Known Issues / Notes

- **Backend Tests:** As mentioned, the backend currently lacks a test suite. Be cautious when refactoring backend logic; manual verification or creating a temporary test script is recommended.
- **Frontend Path:** Note the nested structure `frontend/gol_gym`. Always verify the current working directory before running `ng` commands.

## 7. Example Workflow for Agents

**Task: Add a new field 'address' to the User model.**

1.  **Read:** `backend/main/models/usuario.py` to see existing structure.
2.  **Edit:** Add `address = db.Column(...)`.
3.  **Edit:** Update `to_json`, `from_json`, and validation methods in `usuario.py`.
4.  **Migration:** (If Alembic is configured) Run migration commands.
5.  **Read:** `backend/main/resources/usuario.py` to ensure the new field is handled in API.
6.  **Verify:** Run `python3 backend/app.py` and check if the app starts.

---
*End of Guide*
