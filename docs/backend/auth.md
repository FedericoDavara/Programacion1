# Autenticación y autorización

**Archivos:**
- `backend/main/auth/routes.py` — Blueprint con login/register
- `backend/main/models/permiso.py` — Modelo de permisos
- `backend/main/__init__.py` — Configuración JWT

---

## JWT (JSON Web Tokens)

Se usa **Flask-JWT-Extended** para emitir y validar tokens.

### Configuración

```python
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))  # en segundos
```

El `.env` establece 3600 segundos (1 hora) de expiración.

### Claims del token

Al hacer login, el JWT lleva claims adicionales con información del usuario:

```python
access_token = create_access_token(
    identity=usuario.dni,
    additional_claims={
        "rol":   usuario.rol,
        "dni":   usuario.dni,
        "email": usuario.email
    }
)
```

Estos claims se usan en el backend para autorizar acciones sin consultar la base de datos en cada request.

### Obtener claims en un endpoint

```python
from flask_jwt_extended import get_jwt

claims = get_jwt()
rol   = claims["rol"]
dni   = claims["dni"]
email = claims["email"]
```

---

## Decorator `@role_required`

**Archivo:** `backend/main/auth/` (decorator personalizado)

Este decorator protege endpoints y valida dos cosas:
1. Que el JWT sea válido (firma y expiración).
2. Que exista una fila en la tabla `Permiso` para `{rol_del_token, recurso, método_HTTP}`.

### Uso en un endpoint

```python
class PlanificacionesResource(Resource):
    @role_required(roles=["admin", "profesor"])
    def post(self):
        ...
```

### Lógica interna

```
Request llega
    ↓
Verificar JWT → si inválido → 401
    ↓
Extraer rol del claim
    ↓
Consultar Permiso WHERE rol=? AND recurso=? AND metodo=?
    ↓
Si no existe → 403 Forbidden
    ↓
Ejecutar el método del resource
```

### Implicación importante

Si la tabla `Permiso` está vacía o le falta alguna fila, **el endpoint retornará 403 aunque el JWT sea válido y el rol sea correcto**. La tabla debe estar poblada con todas las reglas necesarias antes de usar el sistema.

---

## Sistema de permisos por rol

### Comportamiento esperado por rol

| Recurso | Método | admin | profesor | user (alumno) |
|---------|--------|-------|----------|---------------|
| `/usuarios` | GET | ✓ | ✓ | — |
| `/usuarios` | POST | ✓ | — | — |
| `/usuario/<dni>` | GET | ✓ | ✓ | ✓ (solo el suyo) |
| `/usuario/<dni>` | PUT | ✓ | ✓ (solo alumnos) | — |
| `/usuario/<dni>` | DELETE | ✓ | ✓ (solo alumnos) | — |
| `/usuarios_a` | GET | ✓ | ✓ | — |
| `/planificaciones` | GET | ✓ | ✓ | — |
| `/planificaciones` | POST | ✓ | ✓ | — |
| `/planificacion/<id>` | PUT | ✓ | ✓ | — |
| `/planificacion/<id>` | DELETE | ✓ | ✓ | — |
| `/clases` | POST | ✓ | — | — |
| `/precios` | POST | ✓ | — | — |

Los endpoints marcados como `[público]` en endpoints.md no usan el decorator.

### Restricciones adicionales en código (no solo permisos)

Hay restricciones que no están en la tabla `Permiso` sino hardcodeadas en los resources:

- **PUT /usuario/<dni>:** un profesor solo puede suspender/activar usuarios con `rol='user'`.
- **DELETE /usuario/<dni>:** un profesor solo puede borrar usuarios con `rol='user'`.
- **DELETE /usuario_a/<dni>:** disponible para admin y profesor.

---

## Flujo de login completo

```
1. POST /auth/login { email, password }
   ↓
2. Buscar usuario por email
   → 400 si no existe
   ↓
3. Verificar password con werkzeug check_password_hash
   → 401 si no coincide
   ↓
4. Verificar si usuario está suspendido
   → 403 con fecha y motivo si is_suspended == True
   ↓
5. Generar JWT con claims {rol, dni, email}
   ↓
6. Retornar { dni, email, access_token, nombre, apellido, rol }
```

---

## Flujo de registro completo

```
1. POST /auth/register { dni, nombre, apellido, email, password, telefono, rol, [...] }
   ↓
2. Crear objeto Usuario y validar campos
   → 400 si validación falla
   → 409 si email ya existe
   ↓
3. Si rol == 'user':   crear Alumno con los campos adicionales
   Si rol == 'profesor': crear Profesor con especialidad
   ↓
4. Hacer db.session.add() + commit()
   ↓
5. Enviar email de bienvenida (template: register)
   ↓
6. Retornar 201 con usuario.to_json_complete()
```

---

## Seguridad — observaciones

| Aspecto | Estado actual | Notas |
|---------|--------------|-------|
| Almacenamiento de contraseñas | Hasheado con werkzeug | Correcto |
| Expiración de tokens | 1 hora | Configurable |
| Refresh tokens | No implementado | El usuario debe re-loguearse al expirar |
| CORS | Solo proxy en dev | Falta configurar en producción |
| localStorage para el token | Implementado | Vulnerable a XSS (aceptable para prototipo) |
| HTTPS | No configurado | Necesario en producción |
| Rate limiting | No implementado | Sin protección contra fuerza bruta |
