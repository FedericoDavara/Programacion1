# Plan de acción — Mejoras GOL GYM

Basado en `AUDITORIA.md`. Ordenado por fases: primero lo de bajo esfuerzo y
alto impacto, después lo estructural. Cada fase es independiente — se puede
hacer una sin las otras y el proyecto sigue funcionando.

**Regla general para todas las fases:** trabajar en una rama propia
(`git checkout -b mejora/nombre-corto`), probar manualmente con los 3 roles
(admin, profesor, user) antes de mergear a `main`, y poder explicar el
cambio en una frase de "antes hacía X, ahora hace Y, porque Z" — si no se
puede explicar así de simple, no es para antes de la mesa.

---

## Fase 1 — Seguridad rápida (< 30 min, alto impacto)

Corresponde a los hallazgos 🔴2 y 🟠5 de la auditoría.

1. **Sacar las credenciales precargadas del login.**
   - Archivo: `frontend/gol_gym/src/app/pages/login/login.component.ts` líneas 25-26.
   - Cambiar `email: ['cr7@gmail.com', ...]` y `password: ['madrid15', ...]` por `email: ['', ...]` y `password: ['', ...]`.
   - Verificación: recargar `/login`, confirmar que los campos están vacíos.

2. **Arreglar el `.gitignore` del backend (lista blanca → lista negra).**
   - Archivo: `backend/.gitignore`.
   - Reemplazar el contenido actual por un patrón estándar:
     ```
     __pycache__/
     *.pyc
     *.db
     .env
     bin/ lib/ lib64/ include/ pyvenv.cfg share/
     ```
   - Verificación: crear un archivo Python nuevo de prueba en `backend/main/`, confirmar con `git status` que aparece como "sin seguimiento" (visible) y no queda invisible.

---

## Fase 2 — Retirar la tabla `Permiso` y simplificar `role_required`

Corresponde al hallazgo 🔴1. Es el cambio más delicado porque toca la
autorización de **todos** los endpoints — hacerlo con cuidado y probar cada
rol antes de dar por terminado.

1. **Reescribir el decorador para que use el parámetro que ya recibe.**
   - Archivo: `backend/main/auth/decorators.py`.
   - Reemplazar el cuerpo de `role_required` para que compare directamente
     contra la lista `roles` recibida, sin consultar `PermisoModel`:
     ```python
     def role_required(roles):
         def decorator(fn):
             def wrapper(*args, **kwargs):
                 verify_jwt_in_request()
                 claims = get_jwt()
                 if claims['rol'] not in roles:
                     return 'Rol sin permisos de acceso al recurso', 403
                 return fn(*args, **kwargs)
             return wrapper
         return decorator
     ```
   - Esto es **más simple y fail-closed**: si un endpoint nuevo se protege
     con `@role_required(roles=["admin"])`, queda protegido de una, sin
     depender de cargar filas en ninguna tabla.

2. **Quitar el import de `PermisoModel` en `decorators.py`** (ya no se usa).

3. **Dar de baja los endpoints de administración de permisos.**
   - Archivo: `backend/main/__init__.py` líneas 63-65 — sacar
     `api.add_resource(resources.PermisosResource, "/permisos")` y
     `api.add_resource(resources.PermisoResource, "/permiso/<id>")`.
   - Borrar `backend/main/resources/permiso.py`.

4. **Borrar el modelo y su tabla.**
   - Borrar `backend/main/models/permiso.py` y su import en
     `backend/main/models/__init__.py`.
   - Generar la migración: `flask db migrate -m "drop tabla permiso"` y
     revisar que el script generado solo borre esa tabla (no toque nada
     más) antes de `flask db upgrade`.

5. **Sacar el bloque de seed de permisos.**
   - Archivo: `backend/seed_data.py` líneas 310-327 (todo el bloque
     `"Permisos de cuotas (si faltan)"`).

6. **Actualizar la colección de Postman** para sacar las requests de
   `/permisos` y `/permiso/<id>` si existen.

7. **Probar los 3 roles contra los endpoints más sensibles** (crear
   usuario, borrar usuario, crear cuota, procesar vencimientos) con Postman
   o desde la UI, confirmando que el 403 sigue apareciendo para quien no
   corresponde y el 200/201 para quien sí.

8. **Actualizar `GUIA_REPASO.md`** — la pregunta "¿Cómo funciona el sistema
   de permisos por rol?" en la sección JWT y Seguridad cambia: ya no hay
   tabla `Permiso`, el chequeo es directo contra la lista de roles del
   decorador. Actualizar también la sección de relaciones de base de datos
   si mencionaba `Permiso`.

**Por qué en este orden:** primero se cambia el comportamiento (paso 1) sin
borrar nada, se prueba que funciona igual o mejor, y recién después se
borra el modelo/tabla (pasos 3-5) — así en cualquier punto se puede volver
atrás sin perder la base de datos.

---

## Fase 3 — Dividir el panel de administración en vistas

Corresponde al hallazgo 🟠3. Usa rutas hijas de Angular Router (ya usan el
Router en el proyecto, es la herramienta más "propia" del stack — no hace
falta traer nada nuevo).

1. **Decidir la navegación:** un layout con pestañas (Bootstrap `nav-tabs`)
   que cambian la ruta hija, manteniendo `/vInicio` como ruta padre.

2. **Crear un componente contenedor**, por ejemplo `PanelAdminComponent`
   (`ng generate component pages/panel-admin`), con:
   - Una barra de pestañas (Usuarios / Cuotas / Clases / Precios / Profesores).
   - Un `<router-outlet></router-outlet>` propio para las rutas hijas.

3. **Convertir cada `<app-lista-x>` en la vista de una ruta hija**, en vez
   de estar todas apiladas. En `app-routing.module.ts`:
   ```ts
   {
     path: 'vInicio',
     component: PanelAdminComponent,
     canActivate: [authsessionGuard],
     children: [
       { path: '', redirectTo: 'usuarios', pathMatch: 'full' },
       { path: 'usuarios', component: ListaUsuariosComponent },
       { path: 'cuotas', component: ListaCuotasComponent },
       { path: 'clases', component: ListaClasesComponent },
       { path: 'precios', component: ListaPreciosComponent },
       { path: 'profesores', component: ListaProfesoresComponent },
     ]
   }
   ```

4. **Sacar `<app-lista-x>` de `vista-inicio.component.html`** — ese
   componente puede directamente desaparecer y reemplazarse por
   `PanelAdminComponent`, o quedar como wrapper si se prefiere no tocar el
   nombre de la ruta.

5. **Actualizar los links de navegación** (navbar/sidebar) para que apunten
   a `/vInicio/usuarios`, `/vInicio/cuotas`, etc. en vez de solo `/vInicio`.

6. **Probar que el guard se siga aplicando** a las rutas hijas: con
   `canActivate` en la ruta padre alcanza (Angular lo hereda para
   navegación normal), pero si se navega directo por URL a una hija
   conviene confirmar manualmente.

**Resultado esperado:** cada módulo carga sus datos (llama a su servicio)
solo cuando el admin entra a esa pestaña, en vez de las 5-6 peticiones
simultáneas actuales al entrar a `/vInicio`.

**Cómo defenderlo en la mesa:** "Separamos el panel en rutas hijas del
mismo Angular Router que ya usábamos para el resto de la navegación, así
cada sección de administración pide sus propios datos solo cuando el admin
la abre, en vez de cargar todo de una."

---

## Fase 4 — `HttpInterceptor` para el header de autorización

Corresponde al hallazgo 🟠4. Ya estaba anotado como pendiente en
`retomar.txt`; esta fase lo detalla paso a paso.

1. Generar el interceptor: `ng generate interceptor interceptors/auth`.
2. Implementar `intercept()` para clonar la request agregando el header
   `Authorization: Bearer <token>` leído de `localStorage`, solo si hay
   token.
3. Registrarlo en `app.module.ts` como `HTTP_INTERCEPTORS` (multi: true).
4. **Sacar el armado manual de headers** de los 7 archivos de `services/`
   (las 29 repeticiones detectadas), dejando que el interceptor lo haga
   por todos.
5. Probar login → navegación a una vista protegida → confirmar en la
   pestaña Network del navegador que el header sigue llegando igual.

**Nota:** esta fase puede hacerse en paralelo con la Fase 3, no dependen
una de la otra.

---

## Fase 5 — Limpieza general (housekeeping)

Corresponde a los hallazgos 🟡6, 🟡7, 🟡8 y ⚪10. Bajo riesgo, se puede hacer
de a poco.

1. Reemplazar los 7 `window.location.reload()` por actualización del
   estado del componente con la respuesta del `subscribe(...)` (por
   ejemplo, reasignar `this.arrayUsers` o volver a llamar al método de
   carga en vez de recargar el navegador entero).
2. Sacar o condicionar los 35 `console.log` de debug.
3. Igualar el `Validators.maxLength` del frontend (20) al límite real del
   backend (128) en `login.component.ts` y `lista-usuarios.component.ts`,
   o documentar explícitamente por qué se decide dejarlo en 20.
4. Revisar `Grupo-B.postman_collection.json` y reemplazar los passwords de
   ejemplo (`1234`, `hola123`) por algo que cumpla la validación mínima
   real del backend (6 caracteres), para que la colección no quede
   desactualizada.

---

## Fase 6 (opcional, no crítica para la mesa) — Automatizar vencimientos de cuota

Corresponde al hallazgo 🟡9. Es la más grande y la única que agrega una
dependencia nueva (`APScheduler` o similar) — evaluar si vale la pena antes
de la entrega o dejarla como "trabajo futuro" documentado.

1. Agregar `APScheduler` a `requirements.txt`.
2. Configurar un job diario que llame a la misma lógica de
   `ProcesarVencimientosResource.post()`.
3. Mantener el botón manual como acción de "forzar ahora", además del job
   automático (no hace falta sacarlo).

---

## Orden recomendado si el tiempo es limitado

Si solo se puede hacer una parte antes de la mesa, priorizar en este
orden — cada una es explicable por sí sola y no depende de las siguientes:

1. Fase 1 (rapidísima, buena primera impresión de prolijidad)
2. Fase 2 (el hallazgo más fuerte de la auditoría, buen tema de seguridad
   para hablar en la mesa)
3. Fase 3 (mejora visible en la demo — se nota a simple vista)
4. Fase 4 y 5 (calidad de código, útil si preguntan "¿qué mejorarían?")
5. Fase 6 (dejarla como respuesta a "¿qué le falta al proyecto?")
