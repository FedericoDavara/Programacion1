# Endpoints REST

**Base URL:** `http://localhost:5000`  
**Archivos:** `backend/main/resources/` y `backend/main/auth/routes.py`

Convenciones:
- `[JWT]` = requiere header `Authorization: Bearer <token>`
- `[admin]` = solo rol admin
- `[admin|prof]` = admin o profesor
- `[público]` = sin autenticación

---

## Autenticación — `/auth`

### POST `/auth/login` — `[público]`

Autentica un usuario y devuelve un JWT.

**Body:**
```json
{ "email": "string", "password": "string" }
```

**Respuesta 200:**
```json
{
  "dni": 1234567,
  "email": "user@mail.com",
  "access_token": "eyJ...",
  "nombre": "Juan",
  "apellido": "Perez",
  "rol": "user"
}
```

**Respuesta 403 (suspendido):**
```json
{
  "msg": "Usuario suspendido",
  "fecha_suspension": "2026-07-01T00:00:00",
  "motivo_suspension": "Falta de pago"
}
```

**Errores:** 400 (datos faltantes), 401 (credenciales incorrectas), 403 (suspendido)

---

### POST `/auth/register` — `[público]`

Registra un nuevo usuario. Crea automáticamente el sub-registro (Alumno o Profesor) según el rol.

**Body (alumno):**
```json
{
  "dni": 1234567,
  "nombre": "Juan",
  "apellido": "Perez",
  "email": "juan@mail.com",
  "password": "clave123",
  "telefono": 1155667788,
  "rol": "user",
  "edad": 25,
  "peso": 75.5,
  "altura": 1.78,
  "sexo": "Masculino"
}
```

**Body (profesor):**
```json
{
  "dni": 7654321,
  "nombre": "Carlos",
  "apellido": "Lopez",
  "email": "carlos@mail.com",
  "password": "clave123",
  "telefono": 1144556677,
  "rol": "profesor",
  "especialidad": "Musculación"
}
```

**Respuesta 201:** usuario.to_json_complete()  
**Efecto secundario:** envía email de bienvenida al nuevo usuario.

---

## Usuarios — `/usuarios`, `/usuario/<dni>`

### GET `/usuarios` — `[JWT]`

Lista paginada de usuarios con filtros.

**Query params:**

| Param | Tipo | Descripción |
|-------|------|-------------|
| `page` | int | Número de página (default: 1) |
| `per_page` | int | Items por página (default: 10, max: 30) |
| `rol` | string | Filtra por rol (`admin`, `profesor`, `user`) |
| `search_term` | string | Busca por nombre o apellido |
| `user` | any | Filtra solo alumnos |
| `profesor` | any | Filtra solo profesores |

**Respuesta 200:**
```json
{
  "usuarios": [...],
  "total": 50,
  "pages": 5,
  "page": 1
}
```

**Lógica de búsqueda:** si `search_term` tiene 1 palabra, busca en nombre O apellido. Si tiene 2 palabras, busca una en nombre y otra en apellido.  
**Orden:** alfabético por nombre.

---

### POST `/usuarios` — `[admin]`

Crea un nuevo usuario.

**Body:** campos de Usuario.from_json()  
**Respuesta 201:** usuario.to_json()

---

### GET `/usuario/<dni>` — `[JWT]`

Retorna un usuario con todos sus datos (incluyendo alumno/profesor relacionado).

**Respuesta 200:** usuario.to_json_complete()  
**Errores:** 404 si no existe

---

### PUT `/usuario/<dni>` — `[JWT]`

Actualiza datos generales del usuario. También gestiona la suspensión/activación.

**Body (actualización general):**
```json
{
  "nombre": "...",
  "apellido": "...",
  "email": "...",
  "telefono": 12345678
}
```

**Body (suspender usuario):**
```json
{
  "fecha_suspension": "2026-07-01T00:00:00",
  "motivo_suspension": "Falta de pago"
}
```

**Body (activar usuario — levantar suspensión):**
```json
{
  "fecha_suspension": null
}
```

**Respuesta (suspensión/activación) 200:**
```json
{
  "usuario": {...},
  "mail_sent": true,
  "action": "suspension"
}
```

**Restricciones:**
- Un profesor solo puede suspender/activar alumnos (`rol='user'`).
- Al suspender: envía email template `suspension`.
- Al activar: envía email template `activacion`.

---

### DELETE `/usuario/<dni>` — `[admin|prof]`

Elimina un usuario. Los profesores solo pueden borrar alumnos.

**Respuesta 204** (sin body)

---

## Alumnos — `/usuarios_a`, `/usuario_a/<dni>`

### GET `/usuarios_a` — `[admin|prof]`

Lista paginada de alumnos con filtros y orden.

**Query params:**

| Param | Descripción |
|-------|-------------|
| `page`, `per_page` | Paginación |
| `nombre` | Filtra por nombre (búsqueda parcial) |
| `apellido` | Filtra por apellido |
| `nrPlanificaciones` | Filtra por cantidad de planificaciones |
| `sortby_nombre` | Ordena por nombre (`asc`/`desc`) |
| `sortby_apellido` | Ordena por apellido |
| `sortby_nrPlanificaciones` | Ordena por cantidad de planificaciones |

---

### POST `/usuarios_a` — `[admin]`

Crea el sub-registro de Alumno para un Usuario existente.  
**Body:** campos de Alumno.from_json()  
**Respuesta 201:** alumno.to_json()

---

### GET `/usuario_a/<dni>` — `[JWT]`

Retorna alumno con todas sus planificaciones.  
**Respuesta 200:** alumno.to_json_complete()

---

### PUT `/usuario_a/<dni>` — `[admin]`

Actualiza datos del alumno (edad, peso, altura, sexo).  
**Respuesta 201:** alumno actualizado

---

### DELETE `/usuario_a/<dni>` — `[admin|prof]`

Elimina el sub-registro de Alumno.  
**Respuesta 204**

---

## Profesores — `/usuarios_p`, `/usuario_p/<dni>`

### GET `/usuarios_p` — `[público]`

Lista todos los profesores. Usado en la página pública del gimnasio.  
**Respuesta 200:** array con `{dni, especialidad, nombre, apellido, foto, descripcion}`

---

### POST `/usuarios_p` — `[admin]`

Crea el sub-registro de Profesor para un Usuario existente.  
**Body:** campos de Profesor.from_json()  
**Respuesta 201:** profesor.to_json()

---

### GET `/usuario_p/<dni>` — `[público]`

Retorna datos básicos de un profesor.  
**Respuesta 200:** profesor.to_json()

---

### PUT `/usuario_p/<dni>` — `[admin]`

Actualiza datos del profesor (especialidad, foto, descripcion).  
**Respuesta 200:** profesor actualizado

---

## Planificaciones — `/planificaciones`, `/planificacion/<id>`

### GET `/planificaciones` — `[JWT]`

Lista paginada de planificaciones con filtros.

**Query params:**

| Param | Descripción |
|-------|-------------|
| `page`, `per_page` | Paginación |
| `profesor` | Filtra por DNI del profesor |
| `alumno` | Filtra por DNI del alumno |
| `fecha` | Filtra por fecha |
| `sortby_*` | Ordenamiento |

---

### POST `/planificaciones` — `[admin|prof]`

Crea una nueva planificación.

**Body:**
```json
{
  "descripcion": "Rutina de fuerza",
  "fecha": "2026-06-14",
  "lunes": "Sentadillas 3x10, Press banca 3x8",
  "martes": "Cardio 30min",
  "miercoles": null,
  "jueves": "Piernas 4x12",
  "viernes": "Hombros y brazos",
  "sabado": null,
  "alumno_dni": 1234567,
  "profesor_dni": 7654321
}
```

**Respuesta 201:** planificación creada  
**Efecto secundario:** envía email al alumno con template `nueva_planificacion`.

---

### GET `/planificacion/<id>` — `[JWT]`

Retorna una planificación con sus datos y objetos alumno/profesor.  
**Respuesta 200:** planificacion.to_json()

---

### PUT `/planificacion/<id>` — `[admin|prof]`

Actualiza una planificación existente.  
**Body:** mismos campos que POST, todos opcionales  
**Respuesta 200:** planificación actualizada  
**Efecto secundario:** envía email al alumno con template `planificacion_actualizada`.

---

### DELETE `/planificacion/<id>` — `[admin|prof]`

Elimina una planificación.  
**Respuesta 204**

---

### GET `/planificacion_a/<dni>` — `[JWT]`

Retorna todas las planificaciones de un alumno.  
**Respuesta 200:** array de planificaciones

---

### GET `/planificacion_p/<dni>` — `[JWT]`

Retorna todas las planificaciones creadas por un profesor.  
**Respuesta 200:** array de planificaciones

---

### GET `/planificaciones_ps` — `[JWT]`

Filtra planificaciones por `dni_profesor` (query param).  
**Respuesta 200:** `{ "planificaciones": [...] }`

---

## Clases — `/clases`, `/clase/<id>`

### GET `/clases` — `[público]`

Lista todas las clases disponibles.  
**Respuesta 200:** array de clases con sus profesores

---

### POST `/clases` — `[admin]`

Crea una nueva clase y asocia profesores.

**Body:**
```json
{
  "nombre": "Spinning",
  "dia": "Lunes",
  "horario": "08:00",
  "imagen": "http://...",
  "profesores": [7654321, 9876543]
}
```

**Respuesta 201:** clase creada con sus profesores

---

### GET `/clase/<id>` — `[público]`

Retorna una clase específica.

---

### PUT `/clase/<id>` — `[admin]`

Actualiza datos de una clase.  
**Respuesta 200:** clase actualizada

---

### DELETE `/clase/<id>` — `[admin]`

Elimina una clase (y sus relaciones en `procla`).  
**Respuesta 204**

---

### GET `/clases_por_profesor/<dni_profesor>` — `[público]`

Retorna todas las clases que dicta un profesor.  
**Respuesta 200:** array de clases

---

## Precios — `/precios`, `/precio/<id>`

### GET `/precios` — `[público]`

Lista todos los planes/precios.  
**Respuesta 200:** array de precios

---

### POST `/precios` — `[admin]`

Crea un nuevo precio/plan.  
**Body:** `{ "nombre": "Plan Mensual", "precio": "$12.000", "descripcion": "..." }`  
**Respuesta 201:** precio creado

---

### GET `/precio/<id>` — `[público]`

Retorna un precio específico.

---

### PUT `/precio/<id>` — `[admin]`

Actualiza un precio.  
**Respuesta 200:** precio actualizado

---

### DELETE `/precio/<id>` — `[admin]`

Elimina un precio.  
**Respuesta 204**

---

## Permisos — `/permisos`, `/permiso/<id>`

### POST `/permisos` — `[admin]`

Crea una nueva regla de permiso.  
**Body:** `{ "rol": "profesor", "recurso": "main.resources.planificacion.Planificaciones", "metodo": "POST" }`  
**Respuesta 201:** permiso creado

---

### PUT `/permiso/<id>`

Actualiza una regla de permiso.  
**Respuesta 200:** permiso actualizado
