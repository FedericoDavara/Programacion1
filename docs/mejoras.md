# Posibles mejoras y preguntas sobre el proyecto

Este documento analiza puntos débiles de la arquitectura actual, funcionalidades faltantes, y preguntas que pueden surgir al estudiar el código o en una evaluación.

---

## Bugs / Funcionalidades incompletas

### 1. Endpoint `/contacto` no implementado en backend
**Dónde:** `backend/main/__init__.py` línea 75 (comentado), `frontend/.../contacto.service.ts`  
**Problema:** El formulario de contacto en la Home existe y llama al servicio, pero la ruta está comentada en el backend. El formulario enviará siempre un error 404.  
**Solución:** Descomentar y completar el endpoint, o eliminar el formulario del frontend si no se va a usar.

### 2. Guard no valida expiración del token
**Dónde:** `guards/authsession.guard.ts`  
**Problema:** Solo verifica que `localStorage.getItem('token')` no sea null. Un token expirado pasa el guard y solo falla al llegar al backend (el usuario ve errores 401 sin entender por qué).  
**Solución:** Usar `jwt-decode` en el guard para verificar el campo `exp` del payload.

### 3. Pérdida de contexto al refrescar la página en `/vPerfil` o `/vPlanif`
**Dónde:** `components/perfil/perfil.component.ts`, `components/planificacion/planificacion.component.ts`  
**Problema:** El DNI se pasa via `history.state`. Si el usuario recarga la página, `history.state` se pierde y el componente no sabe qué DNI mostrar.  
**Solución:** Leer el DNI del token JWT como fallback: `UsuariosService.getUserDNIFromToken()`. Para un admin/profesor viendo el perfil de otro usuario, guardar el DNI en la URL como param (`/vPerfil/:dni`).

### 4. No hay refresh tokens
**Dónde:** `backend/main/__init__.py`, `services/auth.service.ts`  
**Problema:** El JWT expira en 1 hora. No hay endpoint de refresh. El usuario debe volver a loguearse manualmente.  
**Solución:** Implementar endpoint `POST /auth/refresh` con Flask-JWT-Extended y en el frontend hacer el refresh automático antes de que expire.

### 5. Headers HTTP hardcodeados en cada servicio
**Dónde:** todos los archivos en `services/`  
**Problema:** Cada servicio construye sus headers manualmente. Si cambia la clave en `localStorage`, hay que actualizarlo en 5+ archivos.  
**Solución:** Crear un `HttpInterceptor` que agregue el header de forma centralizada.

### 6. `precio` guardado como String
**Dónde:** `backend/main/models/precio.py`  
**Problema:** El precio es un string (`"$12.000"`), lo que imposibilita ordenar por precio o aplicar descuentos programáticamente.  
**Solución:** Guardar como `Float` (o `Integer` en centavos) y formatear en la UI.

### 7. Planificación sin campo para domingo
**Dónde:** `backend/main/models/planificacion.py`  
**Problema:** Hay campos para lunes a sábado pero no para domingo.  
**Solución:** Agregar campo `domingo` al modelo y migrar la DB (`flask db migrate`).

---

## Mejoras de seguridad

### 8. Token en localStorage (XSS vulnerable)
**Nivel:** medio para un prototipo educativo  
**Problema:** `localStorage` es accesible desde JavaScript. Un ataque XSS podría robar el token.  
**Alternativa:** Usar `httpOnly cookies` para almacenar el token (el browser las envía automáticamente y son inaccesibles desde JS).

### 9. Sin protección contra fuerza bruta en login
**Dónde:** `backend/main/auth/routes.py`  
**Problema:** No hay rate limiting. Se pueden probar contraseñas indefinidamente.  
**Solución:** `Flask-Limiter` para limitar intentos de login por IP.

### 10. CORS no configurado para producción
**Dónde:** `backend/main/__init__.py`  
**Problema:** El proxy de Angular funciona en desarrollo, pero en producción el frontend y backend corren en dominios distintos y el browser bloqueará los requests.  
**Solución:** `flask-cors` con origins específicos.

### 11. Contraseña con largo máximo corto (20 chars)
**Dónde:** `backend/main/models/usuario.py`  
**Problema:** El límite de 20 caracteres para contraseñas es muy corto para estándares modernos.  
**Solución:** Subir a al menos 64 o 128 caracteres.

---

## Mejoras de arquitectura

### 12. Sin state management centralizado en Angular
**Estado:** la sesión vive en `localStorage` y cada componente lo lee directamente.  
**Alternativa:** Un `AuthService` como único punto de verdad usando `BehaviorSubject` observable, o NgRx si el proyecto crece.

### 13. Permisos en tabla Permiso — dependencia operacional
**Problema:** Si la tabla `Permiso` está vacía, ningún endpoint protegido funciona aunque los roles sean correctos. No hay seed de datos inicial documentado.  
**Mejora:** Documentar qué filas deben existir y proveer un script de seed (`seed.py`).

### 14. SQLite no apto para múltiples usuarios concurrentes
**Problema:** SQLite tiene limitaciones de concurrencia (un escritor a la vez). Para producción real hay que migrar.  
**Alternativa:** PostgreSQL. Flask-SQLAlchemy y Flask-Migrate soportan el cambio sin modificar el código de modelos.

### 15. Ninguna clase de test (unit ni integration)
**Problema:** No hay archivos de tests en backend ni frontend.  
**Impacto:** Cualquier refactor puede romper funcionalidades sin saberlo.  
**Solución backend:** `pytest` + `pytest-flask` + base de datos en memoria (SQLite in-memory).  
**Solución frontend:** `Jasmine` + `Karma` (ya incluidos en `package.json`).

---

## Funcionalidades que podrían sumarse

| Funcionalidad | Descripción |
|---------------|-------------|
| Búsqueda avanzada de alumnos | Filtrar por rango de edad, peso o cantidad de planificaciones |
| Historial de planificaciones | Actualmente solo se ve la última. Poder ver el historial completo |
| Adjuntar archivos | Imágenes de ejercicios o PDFs en las planificaciones |
| Notificaciones en tiempo real | WebSockets (Flask-SocketIO) para avisar cuando se crea/actualiza planificación |
| Dashboard de estadísticas | Gráficos de alumnos activos, clases más populares, etc. |
| Sistema de asistencia | Registrar si el alumno asistió a cada clase |
| Pagos | Integrar con una pasarela de pagos y vincular con el estado de la cuenta |
| Lazy loading | Las rutas de Angular podrían usar lazy loading para mejorar el tiempo de carga inicial |
| Modo oscuro | Toggle de tema en el frontend |
| i18n | Internacionalización del frontend |

---

## Preguntas frecuentes sobre el diseño

**¿Por qué el DNI es la Primary Key y no un id autoincremental?**  
Porque el DNI argentino es único por persona y es el identificador natural del dominio. Evita tener que manejar dos identificadores. La desventaja es que si el DNI se carga mal, el error es más difícil de corregir (no se puede cambiar una PK con datos relacionados sin borrar y recrear).

**¿Por qué hay dos tablas separadas (Usuario + Alumno / Profesor)?**  
Patrón de herencia de tabla (Table Inheritance). Permite que un Usuario sea un Alumno, un Profesor o un Admin sin columnas null innecesarias. El trade-off es que algunas consultas requieren JOIN entre las dos tablas.

**¿Por qué los permisos están en la base de datos y no en el código?**  
Para poder cambiar permisos sin deployar nuevo código. Un admin podría modificar permisos desde la interfaz. El riesgo es que si la tabla se corrompe o está vacía, el sistema queda bloqueado.

**¿Por qué `precio` es un String y no un número?**  
Decisión de diseño para flexibilidad de formato (`"$12.000"`, `"USD 150"`, `"Gratis"`). La desventaja ya se mencionó en mejoras.

**¿Por qué no hay lazy loading en Angular?**  
El proyecto es relativamente pequeño (13 componentes, bundle ~3.85 MB). Para un proyecto educativo está bien. En producción con más módulos sería necesario.

**¿Qué pasa si se elimina un Usuario que tiene Planificaciones?**  
El modelo `Usuario` tiene `cascade="all, delete-orphan"` hacia `Alumno` y `Profesor`. A su vez, `Planificacion` tiene FK a `Alumno` y `Profesor`. Si la base de datos tiene `ON DELETE CASCADE` configurado o SQLAlchemy maneja la cascada, las planificaciones se eliminarán también. Vale la pena verificarlo con una prueba.
