# Servicios Angular

**Ruta base:** `frontend/gol_gym/src/app/services/`

Todos los servicios usan `HttpClient` inyectado. Las rutas llevan el prefijo `/api` que el proxy de desarrollo redirige a `http://localhost:5000`.

## Headers HTTP

Los servicios que requieren autenticación construyen los headers así:

```typescript
const auth_token = localStorage.getItem('token');
const headers = new HttpHeaders({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${auth_token}`
});
```

Los endpoints públicos (clases, precios, profesores) no incluyen el header `Authorization`.

**Nota:** No hay un interceptor HTTP centralizado. Cada servicio construye sus propios headers manualmente. Esto es una fuente potencial de inconsistencias (ver [mejoras.md](../mejoras.md)).

---

## AuthService
**Archivo:** `services/auth.service.ts`

Gestiona login y logout.

```typescript
login(dataLogin: { email: string, password: string }): Observable<any>
```
- `POST /api/auth/login`
- Al recibir respuesta exitosa, guarda en `localStorage`:
  - `token` → JWT
  - `role` → rol del usuario
  - `dni` → DNI
  - `nombre` → nombre
  - `apellido` → apellido
- Retorna el observable para que el componente maneje la redirección.

```typescript
logout(): void
```
- Limpia las 5 claves de `localStorage`.
- Navega a `/home`.

---

## UsuariosService
**Archivo:** `services/usuarios.service.ts`

El servicio más completo. Gestiona todas las operaciones sobre usuarios, alumnos y profesores.

```typescript
getUsers(page, perPage, filtroRol): Observable
```
`GET /api/usuarios?page=&per_page=&rol=` con JWT.

```typescript
getUserDNIFromToken(): number | null
```
Decodifica el JWT en `localStorage` usando `jwt-decode` y retorna el `dni` del claim.

```typescript
getUser(userDNI): Observable
```
`GET /api/usuario/{dni}` con JWT.

```typescript
getUserAlum(userDNI): Observable
```
`GET /api/usuario_a/{dni}` con JWT.

```typescript
getUserProf(userDNI): Observable
```
`GET /api/usuario_p/{dni}` con JWT (puede ser sin auth, depende del endpoint).

```typescript
searchUsers(searchTerm, filtroRol): Observable
```
`GET /api/usuarios?search_term=&rol=` con JWT.

```typescript
registerUser(userData): Observable
```
`POST /api/auth/register` (sin auth).

```typescript
updateUser(dni, userData): Observable
```
`PUT /api/usuario/{dni}` con JWT.

```typescript
deleteUser(dni): Observable
```
`DELETE /api/usuario/{dni}` con JWT.

```typescript
createUserAlum(userData): Observable
```
`POST /api/usuarios_a` con JWT.

```typescript
updateUserAlum(dni, userData): Observable
```
`PUT /api/usuario_a/{dni}` con JWT.

```typescript
createUserProf(userData): Observable
```
`POST /api/usuarios_p` con JWT.

```typescript
updateUserProf(dni, userData): Observable
```
`PUT /api/usuario_p/{dni}` con JWT.

```typescript
getAllProf(): Observable
```
`GET /api/usuarios_p` — **sin JWT** (endpoint público).

```typescript
deleteUserAlum(dni): Observable
```
`DELETE /api/usuario_a/{dni}` con JWT.

```typescript
suspendUser(dni, date, reason): Observable
```
`PUT /api/usuario/{dni}` con body `{ fecha_suspension: date, motivo_suspension: reason }`.

```typescript
activateUser(dni): Observable
```
`PUT /api/usuario/{dni}` con body `{ fecha_suspension: null }`.

---

## PlanificacionService
**Archivo:** `services/planificacion.service.ts`

```typescript
getPlanif(userDNI): Observable
```
`GET /api/planificacion_a/{dni}` con JWT. Retorna todas las planificaciones del alumno.

```typescript
createPlanif(planificacionData): Observable
```
`POST /api/planificaciones` con JWT.

```typescript
updatePlanif(id, planificacionData): Observable
```
`PUT /api/planificacion/{id}` con JWT.

```typescript
deletePlanif(id): Observable
```
`DELETE /api/planificacion/{id}` con JWT.

---

## ClasesService
**Archivo:** `services/clases.service.ts`

```typescript
getClases(): Observable
```
`GET /api/clases` — **sin JWT** (público).

```typescript
getClase(claseID): Observable
```
`GET /api/clase/{id}` — **sin JWT**.

```typescript
getClaseProfesor(profDNI): Observable
```
`GET /api/clases_por_profesor/{dni}` — **sin JWT**.

```typescript
createClase(claseData): Observable
```
`POST /api/clases` con JWT.

```typescript
updateClase(id, claseData): Observable
```
`PUT /api/clase/{id}` con JWT.

```typescript
deleteClase(id): Observable
```
`DELETE /api/clase/{id}` con JWT.

---

## PreciosService
**Archivo:** `services/precios.service.ts`

```typescript
getPrecios(): Observable
```
`GET /api/precios` — **sin JWT** (público).

```typescript
getPrecio(precioID): Observable
```
`GET /api/precio/{id}` — **sin JWT**.

```typescript
createPrecio(precioData): Observable
```
`POST /api/precios` con JWT.

```typescript
updatePrecio(id, precioData): Observable
```
`PUT /api/precio/{id}` con JWT.

```typescript
deletePrecio(id): Observable
```
`DELETE /api/precio/{id}` con JWT.

---

## ContactoService
**Archivo:** `services/contacto.service.ts`

```typescript
enviarMensaje(data: { nombre: string, email: string, mensaje: string }): Observable<{ message: string }>
```
`POST /api/contacto`

**Estado:** el endpoint `/contacto` está comentado en el backend (`__init__.py` línea 75). El formulario de contacto en el `HomeComponent` existe en el frontend pero la llamada al backend fallará con 404 hasta que se implemente el endpoint.

---

## Estado de sesión en localStorage

| Clave | Valor | Seteado en | Limpiado en |
|-------|-------|-----------|-------------|
| `token` | JWT string | `AuthService.login()` | `AuthService.logout()` |
| `role` | `admin`/`profesor`/`user` | `AuthService.login()` | `AuthService.logout()` |
| `dni` | número | `AuthService.login()` | `AuthService.logout()` |
| `nombre` | string | `AuthService.login()` | `AuthService.logout()` |
| `apellido` | string | `AuthService.login()` | `AuthService.logout()` |

El guard `authsessionGuard` verifica solo la existencia de `token` (no su validez o expiración).
