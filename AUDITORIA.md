# Auditoría técnica — GOL GYM

Fecha: 28/07/2026. Alcance: `backend/` y `frontend/gol_gym/` (código real, no la
documentación). Metodología: lectura directa de cada módulo, búsqueda de
patrones repetidos (`grep`), y ejecución puntual contra la base de datos real
(`grupob.db`) para confirmar hipótesis (ej. qué permisos están cargados hoy).

Cada hallazgo incluye severidad, evidencia con archivo/línea, por qué importa,
y una idea de cómo explicarlo si te preguntan en la mesa — la idea es que
cada cambio tenga una justificación que puedas decir de memoria, no solo
"lo cambié porque sí".

Convención de severidad: 🔴 Crítico · 🟠 Alto · 🟡 Medio · ⚪ Bajo (housekeeping).

---

## 🔴 1. El parámetro `roles` de `role_required(roles=[...])` nunca se usa

**Evidencia:** `backend/main/auth/decorators.py` líneas 8-25.
```python
def role_required(roles):              # <- se recibe...
    def decorator(fn):
        def wrapper(*args, **kwargs):
            ...
            rol = claims['rol']
            exists = db.session.query(PermisoModel).filter(PermisoModel.recurso == resource).first()
            if exists:
                rol_not_permitted = db.session.query(PermisoModel)...scalar() is None
                if rol_not_permitted:
                    return 'Rol sin permisos de acceso al recurso', 403
            return fn(*args, **kwargs)   # <- ...pero "roles" jamás se lee acá
        return wrapper
    return decorator
```
La variable `roles` que le pasás en cada endpoint (`@role_required(roles=["admin"])`,
25 veces en el código) es **puramente decorativa**: la función nunca la
consulta. La decisión real de permitir o no pasa 100% por una tabla en base
de datos, `Permiso` (rol, recurso, método).

**Por qué importa — comportamiento *fail-open*:** si para un recurso nuevo
todavía no cargaste filas en `Permiso`, la condición `if exists:` da `False`
y el decorador **deja pasar a cualquier usuario autenticado**, sin importar
su rol. Esto ya pasó en este proyecto: el comentario en
`backend/seed_data.py` línea 310 (`"Permisos de cuotas (si faltan)"`) muestra
que los endpoints de `/cuotas` estuvieron un tiempo protegidos "de mentira"
hasta que alguien se acordó de cargar las 6 filas correspondientes.

**Verificación en vivo (hecha en esta auditoría):** consultando `grupob.db`
hoy hay 30 filas en `Permiso`, cubriendo la mayoría de los recursos actuales.
El sistema **funciona** porque alguien las cargó a mano en algún momento
(no hay un script que las genere todas), pero un compañero nuevo que agregue
un endpoint y no sepa de esta tabla lo deja sin protección real sin darse
cuenta — y el código no avisa de ningún modo.

**Cómo explicarlo en la mesa:** "Detectamos que el chequeo de rol dependía
de una tabla en base de datos en vez del parámetro que ya recibía la
función, lo cual era redundante y además inseguro por defecto (fail-open).
Lo simplificamos usando directamente la lista de roles que ya se declara en
cada endpoint." → ver Fase 2 del plan de acción.

---

## 🔴 2. Credenciales reales precargadas en el formulario de login

**Evidencia:** `frontend/gol_gym/src/app/pages/login/login.component.ts` líneas 24-27.
```ts
this.loginForm = this.formBuilder.group({
  email: ['cr7@gmail.com', [Validators.required, Validators.email]],
  password: ['madrid15', [Validators.required, Validators.minLength(6), Validators.maxLength(20)]]
})
```
El formulario de login arranca con un usuario **admin** real ya tipeado.
Es cómodo para probar en desarrollo, pero si esto llegara a producción
cualquiera que abra la página ve las credenciales de administrador
apenas mira el código fuente del componente (no hace falta ni loguearse).

**Por qué importa:** es un descuido típico de desarrollo que queda en el
código y es fácil de pasar por alto antes de una demo o entrega.

**Cómo explicarlo en la mesa:** "Era un valor de conveniencia para no
tipear en cada recarga durante el desarrollo; lo sacamos antes de la
entrega final para no exponer una contraseña real en el bundle."

---

## 🟠 3. El panel de administración es una sola página con 6 componentes apilados

**Evidencia:** `frontend/gol_gym/src/app/pages/vista-inicio/vista-inicio.component.html` (10 líneas, completo):
```html
<app-navclose></app-navclose>
<app-lista-cuotas></app-lista-cuotas>
<app-lista-usuarios></app-lista-usuarios>
<app-lista-clases></app-lista-clases>
<app-lista-precios></app-lista-precios>
<app-lista-profesores></app-lista-profesores>
```
`VistaInicioComponent` (el `.ts`) está vacío — ni siquiera tiene lógica,
solo apila los 6 componentes uno debajo del otro. Es la vista que ve un
`admin` o `profesor` al loguearse.

**Por qué importa:** todos los módulos (cuotas, usuarios, clases, precios,
profesores) se renderizan **al mismo tiempo**, en la misma URL, uno debajo
del otro. Cada uno de esos componentes hace sus propias peticiones HTTP al
montar (`ngOnInit`), así que cada carga de `/vInicio` dispara ~5-6 requests
en simultáneo aunque el usuario solo quiera ver usuarios. Además la
navegación es "scrollear hasta encontrar la sección", no hay pestañas ni
rutas propias por módulo.

**Cómo explicarlo en la mesa:** "El panel de admin creció orgánicamente
agregando un componente nuevo por funcionalidad, sin pensar la navegación.
Lo dividimos en rutas hijas para que cada módulo cargue solo cuando el
admin lo abre." → ver Fase 3 del plan de acción.

---

## 🟠 4. No existe ningún `HttpInterceptor` — el token se agrega a mano 29 veces

**Evidencia:** patrón repetido en casi todos los métodos de
`frontend/gol_gym/src/app/services/*.ts`, por ejemplo
`usuarios.service.ts` líneas 17-21:
```ts
let auth_token = localStorage.getItem('token');
const headers = new HttpHeaders({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${auth_token}`
});
```
Encontramos **29 repeticiones** de este mismo bloque de 4 líneas en los
7 archivos de `services/`.

**Por qué importa:** si mañana cambia el nombre de la clave en
`localStorage`, o se agrega lógica de refresh token, hay que tocar 29
lugares distintos y es fácil olvidarse alguno (bug silencioso: una
petición que "misteriosamente" da 401 porque le faltó el header).

**Cómo explicarlo en la mesa:** "Nos dimos cuenta de que estábamos
repitiendo el mismo bloque en cada método de cada servicio. Un
`HttpInterceptor` centraliza esa lógica en un solo lugar que Angular
aplica automáticamente a cada request saliente." → ver Fase 4.

---

## 🟠 5. `.gitignore` del backend usa lista blanca en vez de lista negra

**Evidencia:** `backend/.gitignore` completo:
```
*
!.gitignore
!seed_data.py
!seed_planes.py
!migrations/
!migrations/**
```
La primera línea (`*`) ignora **todo** dentro de `backend/`. Las líneas
siguientes son excepciones puntuales. Los archivos que hoy están
versionados (`app.py`, `main/`, `requirements.txt`, etc.) siguen apareciendo
en `git status` como "limpio" solo porque **ya estaban trackeados antes**
de que existiera esta regla — Git no vuelve a ignorar algo que ya sigue.

**Por qué importa:** cualquier archivo **nuevo** que se cree dentro de
`backend/` (un modelo nuevo, un recurso nuevo, una carpeta nueva) queda
invisible para Git por defecto, salvo que alguien sepa que tiene que
agregar una excepción a mano o forzar el `git add`. Ya lo vimos en esta
misma sesión: `backend/migrations/versions/__pycache__/` aparece como
"sin seguimiento" en vez de "ignorado" porque la excepción
`!migrations/**` reactiva todo lo de adentro, incluyendo carpetas que sí
deberían ignorarse (`__pycache__`).

**Cómo explicarlo en la mesa:** "Es un patrón de lista blanca que
funcionaba cuando el proyecto era chico, pero ahora genera falsos
'archivo sin trackear' y esconde archivos nuevos sin avisar. Lo
reemplazamos por una lista negra estándar (ignorar `.env`, `*.db`,
`__pycache__`, el propio venv) que es el patrón habitual en proyectos
Python."

---

## 🟡 6. `window.location.reload()` para refrescar datos (7 ocurrencias)

**Evidencia:** `frontend/gol_gym/src/app/components/planificacion/planificacion.component.ts`
y `frontend/gol_gym/src/app/components/perfil/perfil.component.ts`, por
ejemplo:
```ts
crearAlumno(dataAlum: any = {}) {
  this.usuariosService.createUserAlum(dataAlum).subscribe(
    (response) => {
      console.log('Alumno creado con éxito', response);
      window.location.reload();   // <- recarga TODA la app
    }, ...
  );
}
```
**Por qué importa:** en vez de actualizar el estado del componente con la
respuesta del backend (que ya la tiene disponible en `response`), se
recarga el navegador entero. Esto pierde cualquier otro estado en pantalla,
genera un parpadeo visible y vuelve a pedir absolutamente todo de nuevo al
backend (token incluido, otra vez el login guard, etc.).

**Cómo explicarlo en la mesa:** "Era la forma más rápida de ver los datos
actualizados durante el desarrollo. La forma correcta en Angular es
reasignar la variable del componente con la respuesta del observable, sin
recargar la página."

---

## 🟡 7. 35 `console.log` de debug sin limpiar

**Evidencia:** `grep -rn "console.log" frontend/gol_gym/src/app` → 35
resultados, distribuidos en casi todos los componentes de formularios
(`perfil.component.ts`, `planificacion.component.ts`, `login.component.ts`, etc).

**Por qué importa:** no es un problema de seguridad grave (no hay
contraseñas en texto plano en esos logs), pero ensucia la consola del
navegador en producción y expone la forma interna de los datos (nombres de
campos, estructura de respuestas) a cualquiera que abra las devtools.

**Cómo explicarlo en la mesa:** "Son logs que dejamos durante el desarrollo
para debuggear los formularios reactivos; antes de entregar los sacamos o
los dejamos condicionados a un flag de entorno de desarrollo."

---

## 🟡 8. Inconsistencia en el límite de caracteres de la contraseña

**Evidencia:** el modelo (`backend/main/models/usuario.py` línea 47) permite
hasta **128** caracteres, pero los formularios reactivos del frontend
(`login.component.ts` línea 26, `lista-usuarios.component.ts` línea 45)
siguen validando `Validators.maxLength(20)`.

**Por qué importa:** es contradictorio — se subió el límite en el backend
(commit `bb684cb`) pero no se actualizó el frontend, así que en la
práctica ningún usuario puede aprovechar el límite nuevo.

**Cómo explicarlo en la mesa:** ya está documentado en `GUIA_REPASO.md`,
sección "Preguntas adicionales". Es un buen ejemplo real de por qué hay que
sincronizar validaciones entre frontend y backend.

---

## 🟡 9. `ProcesarVencimientos` es un botón manual, no un proceso automático

**Evidencia:** `backend/main/resources/cuota.py` líneas 165-171, docstring
del propio código:
```python
class ProcesarVencimientos(Resource):
    """
    Endpoint interno para procesar vencimientos.
    ...
    En producción esto debería ser un cron job o tarea programada.
    """
```
Confirmado que el frontend sí lo llama desde un botón en
`frontend/gol_gym/src/app/components/lista-cuotas/lista-cuotas.component.ts`
línea 103 — no es un endpoint muerto, pero depende de que un admin se
acuerde de tocar el botón para que las cuotas vencidas se procesen
(recargo, suspensión).

**Por qué importa:** es una decisión de diseño válida para un proyecto de
la materia, pero vale la pena poder explicar la diferencia entre "lo
hicimos manual a propósito por tiempo" vs. "no sabíamos que existía
`APScheduler`/cron".

**Cómo explicarlo en la mesa:** "Decidimos exponerlo como acción manual del
admin para no depender de un proceso en background que complicara el
deploy del proyecto de la materia; en un entorno real se automatizaría con
un scheduler."

---

## ⚪ 10. Datos de prueba (emails y contraseñas) commiteados en el Postman collection

**Evidencia:** `backend/Grupo-B.postman_collection.json` (versionado en
git) contiene, por ejemplo, `"password": "1234"`, `"password": "hola123"` y
emails de alumnos de prueba.

**Por qué importa:** son credenciales de prueba, no reales, así que el
riesgo es bajo — pero es un hábito a evitar (`.env`/fixtures separados de
la colección versionada) si el proyecto creciera.

**Cómo explicarlo en la mesa:** "Son datos de prueba para levantar la API
rápido con Postman, no credenciales reales; igual lo ideal sería no
versionarlos junto al resto del código."

---

## ⚪ 11. Sin tests automatizados

Ya documentado como pendiente en `retomar.txt` (pytest para backend,
Jasmine/Karma para frontend). Se confirma en esta auditoría: no hay ningún
archivo `*_test.py` ni `*.spec.ts` con casos reales fuera de los que genera
Angular CLI por defecto (los `.spec.ts` de cada componente están vacíos,
son el boilerplate de `ng generate component`).

---

## Resumen ejecutivo

| # | Hallazgo | Severidad | Esfuerzo estimado |
|---|----------|-----------|--------------------|
| 1 | `role_required` ignora el parámetro `roles` (tabla Permiso fail-open) | 🔴 | Medio |
| 2 | Credenciales precargadas en login | 🔴 | Muy bajo |
| 3 | Panel admin sin dividir en vistas | 🟠 | Medio-Alto |
| 4 | Sin `HttpInterceptor` (29 repeticiones) | 🟠 | Bajo-Medio |
| 5 | `.gitignore` backend en lista blanca | 🟠 | Muy bajo |
| 6 | `window.location.reload()` x7 | 🟡 | Bajo |
| 7 | 35 `console.log` sin limpiar | 🟡 | Muy bajo |
| 8 | Password: 128 backend vs 20 frontend | 🟡 | Muy bajo |
| 9 | Vencimientos de cuota manuales | 🟡 | Medio (opcional) |
| 10 | Datos de prueba en Postman collection | ⚪ | Muy bajo |
| 11 | Sin tests automatizados | ⚪ | Alto (fuera de alcance para la mesa) |

El plan de acción (`PLAN_ACCION.md`) prioriza los ítems 1, 2, 3, 4 y 5 —
son los que más impactan y a la vez son más fáciles de explicar y
demostrar en una mesa de examen.
