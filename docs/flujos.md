# Flujos de usuario

Descripción detallada de los recorridos más importantes del sistema.

---

## 1. Registro de nuevo usuario

```
Frontend                                Backend                         Email
   │                                       │                              │
   │  POST /auth/register                  │                              │
   │  { dni, nombre, apellido, email,      │                              │
   │    password, telefono, rol,           │                              │
   │    [edad, peso, altura, sexo] o       │                              │
   │    [especialidad] }                   │                              │
   │──────────────────────────────────────►│                              │
   │                                       │ Crea Usuario                 │
   │                                       │ Si rol='user' → crea Alumno  │
   │                                       │ Si rol='profesor' → crea Prof│
   │                                       │                              │
   │                                       │──── sendMail(register) ─────►│
   │                                       │                              │
   │  201 usuario.to_json_complete()       │                              │
   │◄──────────────────────────────────────│                              │
```

---

## 2. Login y redirección por rol

```
Usuario ingresa email + password
          │
          ▼
POST /auth/login
          │
          ├── 400: datos faltantes
          ├── 401: credenciales incorrectas
          ├── 403: usuario suspendido
          │         └──► Frontend redirige a /vError?suspended=true&fecha=...&motivo=...
          │
          └── 200: { dni, email, access_token, nombre, apellido, rol }
                    │
                    ▼
            localStorage.setItem(token, role, dni, nombre, apellido)
                    │
                    ▼
              Decodificar JWT con jwt-decode
                    │
                    ├── rol = 'admin' o 'profesor' → navegar a /vInicio
                    └── rol = 'user'               → navegar a /vPerfil
```

---

## 3. Suspensión y activación de usuarios

### Suspender

```
Admin/Profesor en ListaUsuariosComponent
          │
          ▼
Click "Suspender" → formulario pide fecha + motivo
          │
          ▼
PUT /api/usuario/{dni}
{ fecha_suspension: "2026-07-01T00:00:00", motivo_suspension: "Falta de pago" }
          │
          ▼
Backend valida:
  - Si es profesor: solo puede suspender rol='user'
  - Actualiza campos en DB
  - sendMail(suspension) → email al usuario
          │
          ▼
200 { usuario, mail_sent: true, action: 'suspension' }
```

### Efecto en próximo login del usuario suspendido

```
POST /auth/login
          │
          ▼
Backend: usuario.is_suspended == True
          │
          ▼
403 { msg: "Usuario suspendido",
      fecha_suspension: "...",
      motivo_suspension: "..." }
          │
          ▼
Frontend redirige a /vError con queryParams
```

### Activar

```
PUT /api/usuario/{dni}
{ fecha_suspension: null }
          │
          ▼
Backend limpia fecha_suspension
  - sendMail(activacion) → email al usuario
          │
          ▼
200 { usuario, mail_sent: true, action: 'activacion' }
```

---

## 4. Crear planificación para un alumno

```
Profesor/Admin en ListaUsuariosComponent
          │
          ▼
Click "Ver Perfil" en un alumno
  → navegar a /vPerfil con history.state.dni = dni_alumno
          │
          ▼
PerfilComponent carga datos del alumno
  GET /api/usuario/{dni}
  GET /api/usuario_a/{dni}
          │
          ▼
Click "Ver Planificación"
  (requiere que el alumno tenga todos sus datos: edad, peso, altura, sexo)
  → navegar a /vPlanif con history.state.dni = dni_alumno
          │
          ▼
PlanificacionComponent:
  1. Carga profesores → GET /api/usuarios_p (para el dropdown)
  2. Verifica si ya tiene planificación → GET /api/planificacion_a/{dni}
     │
     ├── Tiene planificación → pre-llena formulario (modo edición)
     └── No tiene planificación → formulario vacío (modo creación)
          │
          ▼
Profesor completa: descripcion, fecha, actividades por día, elige profesor en dropdown
          │
          ▼
POST /api/planificaciones
{ descripcion, fecha, lunes, martes, ..., alumno_dni, profesor_dni }
          │
          ▼
Backend:
  1. Crea planificacion en DB
  2. sendMail(nueva_planificacion) → email al alumno con
     subject: "📋 Aviso Importante: Ya actualizamos las rutinas en GOL GYM..."
          │
          ▼
201 planificacion creada → Frontend recarga
```

---

## 5. Alumno consulta su planificación

```
Alumno hace login → redirige a /vPerfil
          │
          ▼
VistaPerfilComponent carga PerfilComponent con su propio dni
(obtenido de localStorage o de history.state)
          │
          ▼
PerfilComponent:
  GET /api/usuario/{dni}
  GET /api/usuario_a/{dni}
          │
          ▼
Puede ver y editar sus datos (nombre, edad, peso, altura, etc.)
          │
          ▼
Si tiene datos completos → botón "Ver Planificación"
  → navegar a /vPlanif
          │
          ▼
PlanificacionComponent:
  GET /api/planificacion_a/{dni} → muestra su rutina semanal
  (el alumno puede editarla también)
```

---

## 6. Admin gestiona clases del gimnasio

```
Admin en /vInicio → tab de Clases
          │
          ▼
ListaClasesComponent:
  GET /api/clases → carga lista
          │
          ├── Crear clase:
          │   POST /api/clases { nombre, dia, horario, imagen, profesores: [dni1, dni2] }
          │   → Backend asocia profesores a la clase en tabla procla
          │
          ├── Editar clase:
          │   PUT /api/clase/{id}
          │
          └── Eliminar clase:
              DELETE /api/clase/{id} → también elimina filas en procla
```

---

## 7. Vista pública (sin login)

```
Visitante en /home (HomeComponent)
          │
          ▼
Se cargan en paralelo:
  GET /api/clases    → muestra horario de clases (ordenado por día/horario)
  GET /api/precios   → muestra planes y precios
  GET /api/usuarios_p → muestra equipo de profesores con fotos y descripciones
          │
          ▼
Formulario de contacto (envía a POST /api/contacto)
  ⚠️  Este endpoint no está implementado en el backend actualmente
```

---

## Resumen de validaciones en 3 niveles

| Campo | Frontend (Reactive Forms) | Backend (setters SQLAlchemy) | DB (constraints) |
|-------|--------------------------|------------------------------|------------------|
| DNI | 7-8 dígitos | — | PK único |
| Email | formato válido | formato válido | UNIQUE, INDEX |
| Password | 6-20 chars | 6-20 chars | — (hasheada) |
| Nombre/Apellido | 2-50 chars, letras | 2-50 chars, letras | NOT NULL |
| Edad | 13-100, entero | 13-100 | NOT NULL |
| Peso | 40-200 | 40-200 | NOT NULL |
| Altura | 1.40-2.20 | 1.40-2.20 | NOT NULL |
| Sexo | dropdown fijo | Masculino/Femenino | NOT NULL |
| Día (clase) | dropdown fijo | Lunes-Domingo | NOT NULL |
| Horario (clase) | regex HH:MM | regex HH:MM | NOT NULL |
