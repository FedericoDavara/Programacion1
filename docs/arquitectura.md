# Arquitectura General

## Diagrama de capas

```
┌─────────────────────────────────────────────────────┐
│                   FRONTEND (Angular 16)              │
│  localhost:4200                                      │
│                                                      │
│  pages/       components/    services/    guards/    │
│  Home         ListaUsuarios  Auth         authsession│
│  Login        ListaClases    Usuarios                │
│  VistaInicio  ListaPrecios   Planificacion           │
│  VistaPerfil  ListaProf      Clases                  │
│  VistaPlanif  Perfil         Precios                 │
│  VistaError   Planificacion  Contacto                │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP (JWT Bearer)
                      │ /api/* → proxy → :5000
                      ▼
┌─────────────────────────────────────────────────────┐
│                   BACKEND (Flask)                    │
│  localhost:5000                                      │
│                                                      │
│  auth/routes.py     ← /auth/login, /auth/register   │
│  resources/         ← todos los endpoints REST       │
│  models/            ← SQLAlchemy ORM                 │
│  mail/              ← Flask-Mail + templates         │
└─────────────────────┬───────────────────────────────┘
                      │ SQLAlchemy
                      ▼
              ┌───────────────┐
              │   SQLite DB   │
              │  grupob.db    │
              └───────────────┘
                      │
              ┌───────────────┐
              │  SMTP Gmail   │
              │  Flask-Mail   │
              └───────────────┘
```

## Patrón de arquitectura

**Backend:** Resource-based REST API.
- Cada recurso es una clase que hereda de `Resource` (Flask-RESTful).
- Los modelos se validan al asignar propiedades (setters SQLAlchemy).
- La autorización se delega a un decorator `@role_required` que consulta la tabla `Permiso`.

**Frontend:** Componentes Angular con servicios inyectados.
- Los servicios encapsulan todas las llamadas HTTP.
- Los componentes consumen los servicios vía inyección de dependencias.
- El estado de sesión vive en `localStorage` (no hay state management centralizado tipo NgRx).

## Roles del sistema

| Rol | Descripción | Acceso principal |
|-----|-------------|-----------------|
| `admin` | Administrador total | Todo |
| `profesor` | Instructor | Gestiona alumnos asignados, crea planificaciones |
| `user` | Alumno | Solo lee su perfil y planificación |

## Flujo de autenticación

```
Login → POST /auth/login → JWT token
        ↓
  localStorage: token, role, dni, nombre, apellido
        ↓
  Cada request HTTP → Header: Authorization: Bearer <token>
        ↓
  Backend → @role_required → valida JWT → consulta tabla Permiso
```

## Tabla de Permisos (dinámica)

El acceso a cada endpoint no está hardcodeado — existe una tabla `Permiso` en la DB con filas `{rol, recurso, metodo}`. El decorator `@role_required` consulta esta tabla en cada request. Esto permite cambiar permisos sin tocar código, pero requiere que la tabla esté correctamente poblada.

## Emails transaccionales

El backend envía emails en 5 situaciones:

| Evento | Template | Destinatario |
|--------|----------|-------------|
| Registro | `register` | Nuevo usuario |
| Suspensión | `suspension` | Usuario suspendido |
| Activación de cuenta | `activacion` | Usuario activado |
| Nueva planificación | `nueva_planificacion` | Alumno |
| Planificación actualizada | `planificacion_actualizada` | Alumno |

## Base de datos — Diagrama entidad-relación

```
Usuario (dni PK)
  ├─── 1:1 ──► Alumno (dni FK)
  │              └─── 1:N ──► Planificacion
  └─── 1:1 ──► Profesor (dni FK)
                 ├─── 1:N ──► Planificacion
                 └─── M:N ──► Clase (via tabla procla)

Permiso (id PK) {rol, recurso, metodo}
Precio  (id PK) {nombre, precio, descripcion}
```

## Proxy de desarrollo

`frontend/gol_gym/proxy.conf.json` redirige `/api/*` → `http://localhost:5000` para evitar CORS en desarrollo. En producción se necesita configurar CORS en el backend o un reverse proxy (nginx).
