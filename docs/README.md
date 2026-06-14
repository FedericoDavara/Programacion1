# GOL GYM — Documentación del Proyecto

Sistema de gestión integral para un gimnasio. Permite administrar usuarios (alumnos, profesores, admin), planificaciones de entrenamiento, clases grupales y precios.

## Stack tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Backend | Python / Flask | 3.1.1 |
| ORM | Flask-SQLAlchemy | 3.1.1 |
| Auth | Flask-JWT-Extended | 4.7.1 |
| Migraciones | Flask-Migrate | 4.1.0 |
| Mail | Flask-Mail | 0.10.0 |
| Base de datos | SQLite | — |
| Frontend | Angular | 16.2.x |
| Estilos | CSS3 puro | — |
| HTTP (front) | HttpClient + RxJS | 7.8.0 |

## Estructura del repositorio

```
Programacion1/
├── backend/
│   ├── app.py                  # Punto de entrada Flask
│   ├── requirements.txt
│   ├── .env                    # Variables de entorno
│   ├── grupob.db               # Base de datos SQLite
│   └── main/
│       ├── __init__.py         # create_app(), registros de rutas
│       ├── models/             # Modelos SQLAlchemy
│       ├── resources/          # Endpoints REST (Flask-RESTful)
│       ├── auth/               # Login, register, blueprints
│       └── mail/               # Funciones de envío de email
├── frontend/
│   └── gol_gym/
│       └── src/app/
│           ├── pages/          # Vistas principales (Home, Login, etc.)
│           ├── components/     # Componentes reutilizables
│           ├── services/       # Servicios HTTP
│           └── guards/         # Guards de ruta
└── docs/                       # Esta carpeta
```

## Índice de documentación

- [Arquitectura general](arquitectura.md)
- [Backend — Modelos de datos](backend/modelos.md)
- [Backend — Endpoints REST](backend/endpoints.md)
- [Backend — Autenticación y permisos](backend/auth.md)
- [Frontend — Componentes](frontend/componentes.md)
- [Frontend — Servicios](frontend/servicios.md)
- [Frontend — Routing y guards](frontend/routing.md)
- [Flujos de usuario](flujos.md)
- [Posibles mejoras y preguntas](mejoras.md)
- [Módulo de Cuotas / Suscripción](backend/cuotas.md)

## Cómo levantar el proyecto

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
# Corre en http://localhost:5000
```

### Frontend
```bash
cd frontend/gol_gym
npm install
npm start
# Corre en http://localhost:4200
```

El frontend usa `proxy.conf.json` para redirigir `/api` a `localhost:5000` en desarrollo.

## Credenciales de prueba

El frontend tiene valores por defecto en el formulario de login:
- Email: `cr7@gmail.com`
- Password: `madrid15`
