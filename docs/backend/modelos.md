# Modelos de datos (SQLAlchemy)

Todos los modelos están en `backend/main/models/`.

---

## Usuario

**Archivo:** `models/usuario.py`  
**Tabla:** `usuario`  
**PK:** `dni` (Integer, 7-8 dígitos)

| Campo | Tipo | Constraints | Validación |
|-------|------|-------------|-----------|
| `dni` | Integer | PK | 7-8 dígitos |
| `nombre` | String(100) | NOT NULL | 2-50 chars, solo letras y espacios, se guarda en Title Case |
| `apellido` | String(100) | NOT NULL | 2-50 chars, solo letras y espacios, se guarda en Title Case |
| `email` | String(250) | NOT NULL, UNIQUE, INDEX | formato email válido |
| `password` | String(100) | NOT NULL | 6-20 chars, se hashea con werkzeug |
| `telefono` | Integer | NOT NULL | 7-15 dígitos |
| `rol` | String(10) | NOT NULL | uno de: `admin`, `profesor`, `user` |
| `fecha_suspension` | DateTime | NULLABLE | — |
| `motivo_suspension` | Text | NULLABLE | — |

**Relaciones:**
- `alumno`: relationship 1:1 → Alumno (cascade delete-orphan)
- `profesor`: relationship 1:1 → Profesor (cascade delete-orphan)

**Propiedades y métodos especiales:**

```python
# Property calculada — True si fecha_suspension > ahora (UTC)
usuario.is_suspended  →  bool

# Setter que hashea y valida la contraseña
usuario.plain_password = "nueva_clave"

# Valida contraseña en texto plano contra el hash guardado
usuario.validate_pass("texto_plano")  →  bool
```

**Métodos de serialización:**

| Método | Incluye |
|--------|---------|
| `to_json()` | Todos los campos + `is_suspended` + `especialidad` si es profesor |
| `to_json_complete()` | `to_json()` + objeto alumno/profesor completo |
| `to_json_short()` | dni, nombre, apellido, teléfono, rol, is_suspended |

---

## Alumno

**Archivo:** `models/alumno.py`  
**Tabla:** `alumno`  
**PK/FK:** `dni` → `usuario.dni`

| Campo | Tipo | Constraints | Validación |
|-------|------|-------------|-----------|
| `dni` | Integer | PK, FK(usuario.dni) | — |
| `edad` | Integer | NOT NULL | 13-100 años |
| `peso` | Float(2) | NOT NULL | 40-200 kg |
| `altura` | Float(2) | NOT NULL | 1.40-2.20 metros |
| `sexo` | String(100) | NOT NULL | `Masculino` o `Femenino` (acepta `m`/`f` y normaliza) |

**Relaciones:**
- `usuario`: relationship → Usuario (back_populates)
- `planificaciones`: relationship 1:N → Planificacion

**Métodos de serialización:**

| Método | Incluye |
|--------|---------|
| `to_json()` | dni, edad, peso, altura, sexo |
| `to_json_complete()` | `to_json()` + array de planificaciones |
| `to_json_short()` | igual a `to_json()` |

---

## Profesor

**Archivo:** `models/profesor.py`  
**Tabla:** `profesor`  
**PK/FK:** `dni` → `usuario.dni`

| Campo | Tipo | Constraints | Validación |
|-------|------|-------------|-----------|
| `dni` | Integer | PK, FK(usuario.dni) | — |
| `especialidad` | String(100) | NOT NULL | 3-50 chars, solo letras y espacios, Title Case |
| `foto` | String(250) | NULLABLE | URL de foto |
| `descripcion` | String(250) | NULLABLE | Bio del profesor |

**Relaciones:**
- `usuario`: relationship → Usuario
- `clases`: relationship M:N → Clase (tabla intermedia `procla`)
- `planificaciones`: relationship 1:N → Planificacion

**Métodos de serialización:**

| Método | Incluye |
|--------|---------|
| `to_json()` | dni, especialidad, foto, descripcion |
| `to_json_complete()` | `to_json()` + array de planificaciones |
| `to_json_short()` | igual a `to_json()` |

---

## Clase

**Archivo:** `models/clase.py`  
**Tabla:** `clase`  
**PK:** `id` (Integer, autoincrement)

| Campo | Tipo | Constraints | Validación |
|-------|------|-------------|-----------|
| `id` | Integer | PK | — |
| `nombre` | String(100) | NOT NULL | 3-50 chars, letras/números/espacios, Title Case |
| `dia` | String(100) | NOT NULL | uno de: Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo |
| `horario` | String(250) | NOT NULL | formato `HH:MM` o `HH:MM-HH:MM` (24h) |
| `imagen` | String(250) | NULLABLE | URL de imagen |

**Relaciones:**
- `profesores`: relationship M:N → Profesor (tabla `procla`)

**Tabla intermedia `procla`:**
```
procla: profesor_dni (FK→profesor.dni), clase_id (FK→clase.id)
```

---

## Planificacion

**Archivo:** `models/planificacion.py`  
**Tabla:** `planificacion`  
**PK:** `id` (Integer, autoincrement)

| Campo | Tipo | Constraints | Validación |
|-------|------|-------------|-----------|
| `id` | Integer | PK | — |
| `descripcion` | String(1000) | NOT NULL | 3-200 chars |
| `fecha` | DateTime | NOT NULL | — |
| `lunes` | String(1000) | NULLABLE | actividades del lunes |
| `martes` | String(1000) | NULLABLE | actividades del martes |
| `miercoles` | String(1000) | NULLABLE | actividades del miércoles |
| `jueves` | String(1000) | NULLABLE | actividades del jueves |
| `viernes` | String(1000) | NULLABLE | actividades del viernes |
| `sabado` | String(1000) | NULLABLE | actividades del sábado |
| `alumno_dni` | Integer | FK(alumno.dni) | — |
| `profesor_dni` | Integer | FK(profesor.dni) | — |

**Relaciones:**
- `alumno`: N:1 → Alumno
- `profesor`: N:1 → Profesor

**Nota:** La planificación es semanal (lunes a sábado). No hay campo para domingo.

---

## Permiso

**Archivo:** `models/permiso.py`  
**Tabla:** `permiso`  
**PK:** `id` (Integer, autoincrement)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | PK |
| `rol` | String(10) | `admin`, `profesor` o `user` |
| `recurso` | String(100) | Nombre completo del recurso (ej: `main.resources.usuario.Usuarios`) |
| `metodo` | String(100) | Método HTTP (`GET`, `POST`, `PUT`, `DELETE`) |

Esta tabla es consultada por el decorator `@role_required` en cada request protegido. Ver [auth.md](auth.md) para más detalle.

---

## Precio

**Archivo:** `models/precio.py`  
**Tabla:** `precio`  
**PK:** `id` (Integer, autoincrement)

| Campo | Tipo | Constraints | Validación |
|-------|------|-------------|-----------|
| `id` | Integer | PK | — |
| `nombre` | String(100) | NOT NULL | 2-50 chars |
| `precio` | String(50) | NOT NULL | string libre (ej: `"$12.000"`) |
| `descripcion` | String(250) | NULLABLE | — |

**Nota:** `precio` se guarda como String para permitir formatos con símbolo y separadores (`$12.000`, `USD 150`).
