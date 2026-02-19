# FRONTEND KNOWLEDGE BASE

## OVERVIEW
Angular 16 Single Page Application for Gym Management.

## STRUCTURE
```
src/app/
├── components/       # Dumb/Smart components (Navbar, Planificacion)
├── pages/            # Route views (Home, Login, VistaPerfil)
├── services/         # API clients (UsuariosService, ClasesService)
├── guards/           # Route protection (AuthGuard)
└── app.module.ts     # Main module registration
```

## KEY PATTERNS
- **Routing**: Defined in `app-routing.module.ts`.
- **HTTP**: Services use `HttpClient` to talk to Flask API.
- **Forms**: Uses both `FormsModule` and `ReactiveFormsModule`.
- **Auth**: JWT stored in localStorage (likely) and attached to requests.

## COMPONENTS
- **Pages**: Top-level views (`vista-planificacion`, `vista-perfil`).
- **Shared**: `navbar`, `navclose`, `alert`.
- **Feature**: `clase`, `lista-usuarios`.

## COMMANDS
```bash
ng generate component components/name
ng generate service services/name
ng serve
```
