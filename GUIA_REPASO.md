# Guía de repaso — Defensa oral Programación I

> **Nota importante:** el pedido original describía el sistema como una rotisería
> ("La Roti", roles Administrador/Cliente/Encargado). El código real de este
> repositorio es **GOL GYM** (gimnasio), con roles `admin`, `profesor` y `user`
> (alumno). Esta guía documenta el proyecto **real** que está en
> `backend/` y `frontend/gol_gym/`, verificado línea por línea contra el código
> actual (28/07/2026). Las preguntas base que me pasaste (de otro proyecto)
> se usaron solo como plantilla de estilo; cada respuesta fue re-verificada acá.

Roles válidos: `admin`, `profesor`, `user` — ver `backend/main/models/usuario.py` línea 130.

---

## JWT y Seguridad

**Pregunta:** ¿Dónde se genera el token y con qué identidad?
**Respuesta:** Se genera en el login con `create_access_token(identity=usuario)`, pasándole el objeto `Usuario` completo (no el DNI). Flask-JWT-Extended usa el `user_identity_loader` para convertir ese objeto en el string que va en el claim `sub`.
**Dónde está en el código:** `backend/main/auth/routes.py` línea 30
```python
access_token = create_access_token(identity=usuario)
```

**Pregunta:** ¿Qué datos contiene el payload del token (additional_claims)?
**Respuesta:** Solo `rol`, `dni` y `email`. El nombre y apellido **no** van en el token: se devuelven aparte en el JSON de la respuesta del login y el frontend los guarda directo en localStorage sin decodificar el token.
**Dónde está en el código:** `backend/main/auth/decorators.py` líneas 31-38
```python
@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {'rol': usuario.rol, 'dni': usuario.dni, 'email': usuario.email}
    return claims
```

**Pregunta:** ¿Cuál es la identidad (`sub`) del token?
**Respuesta:** El DNI del usuario, convertido a string. Lo define el `user_identity_loader`, que Flask-JWT-Extended llama automáticamente al crear el token.
**Dónde está en el código:** `backend/main/auth/decorators.py` líneas 27-29
```python
@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return str(usuario.dni)
```

**Pregunta:** ¿Qué devuelve el endpoint de login además del token?
**Respuesta:** DNI, email, nombre, apellido y rol en texto plano, junto al `access_token`. Esto es lo que el frontend usa para poblar `localStorage` sin tener que decodificar nada (salvo rol y dni, que sí se sacan del token decodificado).
**Dónde está en el código:** `backend/main/auth/routes.py` líneas 30-40

**Pregunta:** ¿Qué datos NO deberían ir en el payload del token?
**Respuesta:** Nada sensible: contraseñas (ni hasheadas), DNI si se quisiera más discreción, datos bancarios o de salud. El payload de un JWT se puede leer libremente con Base64, solo la firma impide modificarlo sin invalidarlo.
**Dónde está en el código:** conceptual — coincide con lo que efectivamente hace `add_claims_to_access_token` (solo rol/dni/email, nada de password).

**Pregunta:** ¿En qué está codificado y firmado el token?
**Respuesta:** Codificado en Base64URL (header y payload legibles por cualquiera) y firmado con HS256 (HMAC-SHA256) usando `JWT_SECRET_KEY`. La firma no oculta el contenido, solo garantiza que no fue modificado.
**Dónde está en el código:** `backend/main/__init__.py` línea 85 — `app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")`

**Pregunta:** ¿Cómo está compuesto el JWT?
**Respuesta:** Header (algoritmo y tipo), Payload (claims: identity, rol, dni, email, exp, iat) y Firma (hash de header+payload+secret key). La firma es lo único que impide falsificar un token sin conocer la clave.
**Dónde está en el código:** conceptual (estándar JWT); la generación puntual está en `routes.py:30` y `decorators.py:31-38`.

**Pregunta:** ¿Cómo se protege una ruta en el backend?
**Respuesta:** Con `@jwt_required()` (solo exige token válido) o con `@role_required(roles=[...])` (exige token válido **y** que el rol del claim esté en la lista `roles` pasada al decorador). Si falta o es inválido, Flask-JWT-Extended devuelve 401 automáticamente.
**Dónde está en el código:** `backend/main/resources/usuario.py` línea 42 (`@jwt_required()`) y línea 51 (`@role_required(roles=["admin","profesor"])`)

**Pregunta:** ¿Cómo funciona el sistema de permisos por rol (`role_required`)? — es lo más particular de este proyecto
**Respuesta:** Es una comparación directa contra la lista `roles` que recibe el decorador, sin consultar la base de datos: si el rol del claim del JWT no está en esa lista, devuelve 403. Antes existía una tabla `Permiso` (rol, recurso, endpoint) consultada en cada request — se sacó porque era **fail-open**: si un endpoint nuevo no tenía filas cargadas en `Permiso`, el chequeo lo dejaba pasar sin restricción por defecto. El enfoque actual es fail-closed: todo endpoint protegido con `@role_required(roles=[...])` queda restringido de una, sin depender de datos en una tabla.
**Dónde está en el código:** `backend/main/auth/decorators.py` líneas 8-19
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

**Pregunta:** ¿Qué pasa cuando el token expira?
**Respuesta:** En el backend, `verify_jwt_in_request()` revisa el claim `exp` automáticamente y devuelve 401 si venció — no hay chequeo manual. En el frontend, el guard de rutas decodifica el token con `jwt-decode`, compara `exp` contra la hora actual, y si venció limpia el `localStorage` y redirige a `home` **antes** de que se dispare el 401.
**Dónde está en el código:** `frontend/gol_gym/src/app/guards/authsession.guard.ts` líneas 14-20
```ts
const { exp } = jwtDecode<{ exp: number }>(token);
if (exp && Date.now() >= exp * 1000) {
  localStorage.clear();
  router.navigateByUrl('home');
  return false;
}
```

**Pregunta:** ¿Cuánto dura el token y dónde se configura?
**Respuesta:** El tiempo de expiración se define en una variable de entorno y se carga como entero de segundos en la config de Flask-JWT-Extended.
**Dónde está en el código:** `backend/main/__init__.py` línea 86 — `app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))` (en `.env-example` vale `3600`, es decir 1 hora)

**Pregunta:** ¿Qué pasa si se filtra la SECRET_KEY?
**Respuesta:** Un atacante podría firmar tokens válidos con cualquier rol (incluso admin), saltándose toda la autenticación. La solución es rotar la clave inmediatamente, lo que invalida todos los tokens existentes y fuerza un nuevo login.
**Dónde está en el código:** conceptual — la clave vive en `backend/main/__init__.py:85`, tomada de `.env` (no versionado, ver `.gitignore`).

**Pregunta:** ¿Cómo llega el token del backend al frontend y de ahí a cada request?
**Respuesta:** El backend lo devuelve en el JSON de `/auth/login`. El componente de login lo guarda en `localStorage`. Como **no hay interceptor HTTP**, cada método de cada `service` arma manualmente un header `Authorization: Bearer <token>` leyendo `localStorage.getItem('token')` antes de cada petición protegida.
**Dónde está en el código:** `frontend/gol_gym/src/app/pages/login/login.component.ts` línea 35 (`localStorage.setItem('token', rta.access_token)`) y `frontend/gol_gym/src/app/services/usuarios.service.ts` líneas 17-21 (armado manual del header)

---

## Angular (componentes, decoradores, guards, interceptor, routing)

**Pregunta:** ¿Qué es el módulo Router y para qué sirve?
**Respuesta:** Es el módulo de Angular encargado de la navegación dentro de una SPA: permite cambiar de vista (componente) sin recargar la página completa, mapeando URLs a componentes.
**Dónde está en el código:** `frontend/gol_gym/src/app/app-routing.module.ts` líneas 11-20
```ts
const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'vInicio', component: VistaInicioComponent, canActivate:[authsessionGuard]},
  { path: 'vPerfil', component: VistaPerfilComponent, canActivate:[authsessionGuard] },
  { path: 'vPlanif', component: VistaPlanificacionComponent, canActivate:[authsessionGuard] },
  { path: '**', redirectTo: 'vError' },
];
```
*Nota:* a diferencia de otros proyectos, acá las rutas **no** tienen `data: { roles: [...] }` — el guard solo valida sesión/expiración, no rol por ruta.

**Pregunta:** ¿Cómo se comunican los componentes padre-hijo?
**Respuesta:** Con `@Input()` (el padre le pasa datos al hijo). En este proyecto no hay ningún `@Output()` implementado — la comunicación hijo→padre se resuelve navegando por rutas (`router.navigate`) en vez de emitir eventos.
**Dónde está en el código:** `frontend/gol_gym/src/app/components/cuota-alumno/cuota-alumno.component.ts` línea 10 (`@Input() dni!: number;`) usado desde `frontend/gol_gym/src/app/pages/vista-perfil/vista-perfil.component.html` línea 5:
```html
<app-cuota-alumno *ngIf="rol === 'user' && dni" [dni]="dni"></app-cuota-alumno>
```

**Pregunta:** ¿Qué decoradores usa Angular?
**Respuesta:** `@Component` (define un componente con selector/template/estilos), `@NgModule` (agrupa componentes/servicios en un módulo), `@Injectable` (marca una clase como servicio inyectable), `@Directive` (comportamiento reutilizable sin template propio) y `@Pipe` (transforma datos en el template). Para comunicación entre componentes: `@Input`/`@Output`.
**Dónde está en el código:** ejemplo real de `@Component` + `@Injectable`: `frontend/gol_gym/src/app/services/auth.service.ts` líneas 6-9 (`@Injectable({providedIn: 'root'})`) y `frontend/gol_gym/src/app/app.module.ts` líneas 25-54 (`@NgModule`)

**Pregunta:** ¿Cómo se protege una ruta con un guard? ¿Es funcional o de clase?
**Respuesta:** Es un **guard funcional** (`CanActivateFn`, sintaxis moderna de Angular), no una clase con `implements CanActivate`. Revisa si hay token en `localStorage` y si no venció; si algo falla, limpia storage y redirige a `home`.
**Dónde está en el código:** `frontend/gol_gym/src/app/guards/authsession.guard.ts` completo
```ts
export const authsessionGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('token');
  if (!token) { router.navigateByUrl('home'); return false; }
  ...
  return true;
};
```
*Importante:* el guard **no** valida el rol contra la ruta (no hay `data.roles` en el routing), solo autenticación + expiración. La restricción por rol se aplica del lado del backend (`role_required`) y ocultando/mostrando botones en el HTML con `*ngIf`.

**Pregunta:** ¿Hay un HttpInterceptor en este proyecto?
**Respuesta:** **No.** Es una mejora pendiente documentada en `retomar.txt`. Actualmente cada `service` arma el header `Authorization` a mano en cada método, repitiendo el mismo bloque de código muchas veces.
**Dónde está en el código:** no existe `*.interceptor.ts` en `frontend/gol_gym/src/app/` (verificado con `find`). Ejemplo del patrón manual repetido: `frontend/gol_gym/src/app/services/usuarios.service.ts` líneas 16-30.

**Pregunta:** ¿Dónde se guarda el token y los datos de sesión en el frontend?
**Respuesta:** Principalmente en `localStorage` (`token`, `role`, `dni`, `nombre`, `apellido`), que sobrevive a cerrar el navegador. La vista de perfil usa además `sessionStorage` para recordar qué DNI se estaba viendo tras un F5, sin pisar el DNI del propio usuario logueado.
**Dónde está en el código:** `frontend/gol_gym/src/app/pages/login/login.component.ts` líneas 35-41 (localStorage) y `frontend/gol_gym/src/app/pages/vista-perfil/vista-perfil.component.ts` líneas 12-29 (sessionStorage con fallback a localStorage)

**Pregunta:** ¿Cómo se conecta Bootstrap con Angular?
**Respuesta:** Por CDN, importado directamente en el `<head>` de `index.html` (CSS, JS bundle e íconos). No se instaló vía npm en el bundle de producción, salvo `bootstrap-icons` que sí está en `angular.json` como estilo global.
**Dónde está en el código:** `frontend/gol_gym/src/index.html` líneas 10-12
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

**Pregunta:** ¿Por qué Bootstrap solo se importa una vez, en `index.html`?
**Respuesta:** Porque Angular es una SPA: `index.html` es el único HTML real que carga el navegador. Angular monta ahí `<app-root>` y desde ese punto renderiza todos los componentes según la ruta, así que cualquier CSS/JS global importado en el `<head>` queda disponible para toda la app.
**Dónde está en el código:** `frontend/gol_gym/src/index.html` línea 17 (`<app-root></app-root>`)

**Pregunta:** Ciclo de vida de un componente — ¿qué usan acá?
**Respuesta:** `ngOnInit` (se ejecuta al crear el componente, se usa para llamadas HTTP iniciales) y `ngOnDestroy` (limpieza al destruir el componente, por ejemplo cancelar un timeout).
**Dónde está en el código:** `frontend/gol_gym/src/app/app.component.ts` líneas 8-19
```ts
export class AppComponent implements OnInit, OnDestroy {
  ngOnInit(): void { this.startTimer(); }
  ngOnDestroy(): void { this.clearTimer(); }
```

**Pregunta:** ¿Qué directivas estructurales y de atributo usa el proyecto?
**Respuesta:** Estructurales: `*ngIf` y `*ngFor` (agregan/quitan del DOM). De atributo: `[ngClass]` (clases condicionales) y `[(ngModel)]` (two-way binding). No encontré uso de `*ngSwitch` ni `ngStyle` en este proyecto.
**Dónde está en el código:** `frontend/gol_gym/src/app/components/lista-usuarios/lista-usuarios.component.html` líneas 6, 27, 35
```html
[(ngModel)]="searchTerm" (input)="buscarUsuarios()"
*ngFor="let user of arrayUsers"
[ngClass]="user.is_suspended ? 'btn-danger' : 'btn-warning'"
```

**Pregunta:** ¿Cómo se manejan los formularios?
**Respuesta:** Con **Reactive Forms** (`FormBuilder`, `FormGroup`, `Validators`), no con template-driven forms puros. Cada formulario grande (login, perfil, planificación, alta de usuario) arma su `FormGroup` en el constructor o en `ngOnInit` con validadores de Angular y validadores custom propios.
**Dónde está en el código:** `frontend/gol_gym/src/app/pages/login/login.component.ts` líneas 24-27
```ts
this.loginForm = this.formBuilder.group({
  email: ['cr7@gmail.com', [Validators.required, Validators.email]],
  password: ['madrid15', [Validators.required, Validators.minLength(6), Validators.maxLength(20)]]
})
```

**Pregunta:** ¿Cómo se comunica el frontend con el backend?
**Respuesta:** Con `HttpClient` haciendo peticiones REST (GET/POST/PUT/DELETE) en JSON. En desarrollo, `proxy.conf.json` redirige todo lo que empieza con `/api` hacia `http://127.0.0.1:5000`, evitando problemas de CORS mientras se programa.
**Dónde está en el código:** `frontend/gol_gym/proxy.conf.json` completo
```json
{ "/api": { "target": "http://127.0.0.1:5000", "pathRewrite": { "^/api":"" } } }
```

---

## Backend / Flask (modelos, relaciones, paginación, protección de rutas)

**Pregunta:** ¿Cómo se registran las rutas de la API?
**Respuesta:** Con `flask_restful.Api`, registrando cada clase `Resource` a una URL con `api.add_resource(...)`. El login/register son la excepción: van en un `Blueprint` aparte (`auth`) con `@auth.route(...)`.
**Dónde está en el código:** `backend/main/__init__.py` líneas 37-81 (recursos) y línea 91 (`app.register_blueprint(routes.auth)`)

**Pregunta:** ¿Cómo funciona la paginación?
**Respuesta:** Usa el método `.paginate(page=..., per_page=..., max_per_page=30)` de Flask-SQLAlchemy sobre el query, no un cálculo manual de `offset`/`limit`. Devuelve además `total` y `pages` para que el frontend arme los controles de paginación.
**Dónde está en el código:** `backend/main/resources/usuario.py` líneas 267-278
```python
usuarios = usuarios.paginate(page=page, per_page=per_page, error_out=False, max_per_page=30)
return jsonify({"usuarios": [u.to_json() for u in usuarios], "total": usuarios.total, "pages": usuarios.pages, "page": page})
```

**Pregunta:** ¿Cómo se protegen los distintos métodos HTTP de un mismo recurso?
**Respuesta:** Cada método (`get`, `post`, `put`, `delete`) de la clase `Resource` lleva su propio decorador, y pueden ser distintos entre sí: por ejemplo `GET` puede ser público u opcional mientras que `POST`/`DELETE` exigen rol `admin`.
**Dónde está en el código:** `backend/main/resources/usuario.py` — `Usuario.get` usa `@jwt_required()` (línea 42) pero `Usuarios.post` usa `@role_required(roles=["admin"])` (línea 280)

**Pregunta:** ¿Dónde y cómo se validan los datos de un modelo?
**Respuesta:** Con el decorador `@validates` de SQLAlchemy sobre cada campo, que corre automáticamente al asignar el atributo (antes del `commit`) y lanza `ValueError` si el dato es inválido. El recurso captura ese `ValueError` y devuelve 400 con el mensaje.
**Dónde está en el código:** `backend/main/models/usuario.py` líneas 126-133 (validación de rol) y `backend/main/resources/usuario.py` líneas 201-203 (`except ValueError as e: return {"error": str(e)}, 400`)

**Pregunta:** ¿Cómo se guarda la contraseña?
**Respuesta:** Nunca en texto plano. El modelo expone un `@property` llamado `plain_password` que **solo tiene setter**: al asignarle un valor, lo hashea con `generate_password_hash` de Werkzeug y lo guarda en la columna `password`. Intentar leer `plain_password` lanza una excepción.
**Dónde está en el código:** `backend/main/models/usuario.py` líneas 36-48
```python
@property
def plain_password(self):
    raise AttributeError("password cant be read")

@plain_password.setter
def plain_password(self, password):
    ...
    self.password = generate_password_hash(password)
```

**Pregunta:** ¿Qué relación 1:1 existe en el modelo y cómo está resuelta?
**Respuesta:** `Usuario`↔`Alumno` y `Usuario`↔`Profesor`. No es una FK nueva: la clave primaria de `Alumno`/`Profesor` **es a la vez** foreign key al DNI de `Usuario` (herencia por tabla separada). Del lado de `Usuario` se usa `uselist=False` para forzar cardinalidad 1:1.
**Dónde está en el código:** `backend/main/models/alumno.py` línea 7 (`dni = db.Column(db.Integer, db.ForeignKey(UsuarioModel.dni), primary_key=True)`) y `backend/main/models/usuario.py` líneas 21-34 (`db.relationship("Profesor", uselist=False, ...)`)

---

## Base de datos (SQLAlchemy, motor, relaciones 1:1 y 1:N)

**Pregunta:** ¿Qué es SQLAlchemy?
**Respuesta:** Un ORM (Object-Relational Mapper): permite trabajar con la base de datos usando clases y objetos de Python en vez de escribir SQL a mano. Acá se usa vía la extensión `Flask-SQLAlchemy`.
**Dónde está en el código:** `backend/main/__init__.py` línea 12 — `db = SQLAlchemy()`

**Pregunta:** ¿Cómo se cambia el motor de base de datos?
**Respuesta:** Cambiando la cadena de conexión en `SQLALCHEMY_DATABASE_URI`. Hoy apunta a SQLite armando la ruta desde variables de entorno; para otro motor (ej. PostgreSQL) se reemplaza ese string completo por el URI correspondiente (`postgresql://usuario:pass@host/db`).
**Dónde está en el código:** `backend/main/__init__.py` líneas 28-30
```python
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:////" + os.getenv("DATABASE_PATH") + os.getenv("DATABASE_NAME")
)
```

**Pregunta:** ¿Cómo se definen las relaciones entre tablas?
**Respuesta:** Con `db.ForeignKey` (la restricción real a nivel de columna/BD) y `db.relationship` (el atributo Python que permite navegar el objeto relacionado sin escribir el JOIN a mano). SQLAlchemy es quien traduce `relationship` en las queries JOIN necesarias.
**Dónde está en el código:** `backend/main/models/cuota.py` líneas 12 y 21
```python
alumno_dni = db.Column(db.Integer, db.ForeignKey(AlumnoModel.dni), nullable=False)
alumno = db.relationship("Alumno", back_populates="cuotas")
```

**Pregunta:** Mostrame una relación 1:N real del proyecto.
**Respuesta:** Un `Alumno` tiene muchas `Cuota` (y muchas `Planificacion`). La FK vive del lado "muchos" (`Cuota.alumno_dni`), y en `Alumno` se declara la lista con `cascade="all, delete-orphan"` para que al borrar el alumno se borren sus cuotas.
**Dónde está en el código:** `backend/main/models/alumno.py` línea 20 (`cuotas = db.relationship("Cuota", back_populates="alumno", cascade="all, delete-orphan")`) y `backend/main/models/cuota.py` línea 12 (la FK)

**Pregunta:** ¿Hay alguna relación muchos a muchos (N:M)?
**Respuesta:** Sí: `Profesor`↔`Clase`, a través de una tabla intermedia `procla` con dos FKs compuestas como clave primaria (una fila por cada par profesor-clase).
**Dónde está en el código:** `backend/main/models/profesor.py` líneas 6-9 y 18
```python
procla = db.Table("procla",
    db.Column("clase_id", db.Integer, db.ForeignKey("clase.id"), primary_key=True),
    db.Column("profesor_dni", db.Integer, db.ForeignKey("profesor.dni"), primary_key=True))

clases = db.relationship('Clase', secondary=procla, backref=db.backref('profesores', lazy='dynamic'), cascade="all")
```

**Pregunta:** ¿Qué es una migración y por qué se usa flask-migrate en vez de crear las tablas a mano?
**Respuesta:** Una migración es un script versionado que aplica (o revierte) cambios incrementales al esquema de la base de datos, sin perder los datos existentes. `flask db migrate` genera el script comparando modelos vs BD actual, y `flask db upgrade` lo aplica. Crear tablas a mano no deja historial ni permite deshacer cambios de forma segura.
**Dónde está en el código:** `backend/migrations/versions/` (6 migraciones aplicadas, ej. `e7a057d5cd11_add_domingo_to_planificacion.py`) y `backend/main/__init__.py` línea 32 (`migrate.init_app(app, db)`)

---

## CSS / Bootstrap / HTML

**Pregunta:** ¿Qué tipos de selectores CSS se usan en el proyecto?
**Respuesta:** De etiqueta (`h4`, `p`), de clase (`.cuota-card`, la inmensa mayoría) y de id (`#Inicio`, `#Clasesid`, usados como anclas de scroll, no para estilos repetidos). También hay selectores compuestos por combinación de clases (`.cuota-card.estado-al-dia`).
**Dónde está en el código:** `frontend/gol_gym/src/app/components/cuota-alumno/cuota-alumno.component.css` línea 21 (clase compuesta) y `frontend/gol_gym/src/app/pages/home/home.component.css` línea 5 (`#Inicio`)

**Pregunta:** ¿Cuál es el máximo de columnas en una fila del grid de Bootstrap?
**Respuesta:** 12 columnas. Las filas (`.row`) son ilimitadas.
**Dónde está en el código:** conceptual (Bootstrap), usado en `frontend/gol_gym/src/app/components/lista-usuarios/lista-usuarios.component.html` línea 3 (`col-md-8 offset-md-2`)

**Pregunta:** ¿Dónde está el HTML principal de la app?
**Respuesta:** `index.html`, el único HTML real de la SPA. Ahí vive `<app-root>`, el punto donde Angular monta todo, y todos los imports globales (Bootstrap, ícono de la pestaña, título).
**Dónde está en el código:** `frontend/gol_gym/src/index.html` completo

**Pregunta:** ¿Cómo se le indica a Angular dónde va cada CSS?
**Respuesta:** Los estilos globales se listan en `angular.json` (`styles`), y cada componente además puede tener su propio `.css` referenciado en `styleUrls` dentro del `@Component`, con alcance limitado a ese componente.
**Dónde está en el código:** `frontend/gol_gym/angular.json` — array `styles` con `bootstrap-icons/.../bootstrap-icons.css` y `src/styles.css` (Bootstrap en sí NO está acá, se importa por CDN en `index.html`)

**Pregunta:** ¿Qué es el "budget" de CSS en Angular y cuánto está configurado?
**Respuesta:** Un límite que el build de Angular controla para no dejar crecer descontroladamente el bundle: advierte o falla si un componente supera cierto tamaño de CSS, o si el bundle inicial total supera el límite.
**Dónde está en el código:** `frontend/gol_gym/angular.json` — `configurations.production.budgets`: inicial 500kb warning / 1mb error, por componente 6kb warning / 10kb error

---

## Conceptos generales (entornos virtuales, ORM, REST, roles)

**Pregunta:** ¿Qué es un entorno virtual y para qué sirve?
**Respuesta:** Un entorno aislado de Python que permite instalar dependencias de un proyecto sin afectar al sistema ni a otros proyectos. Evita conflictos de versiones y hace el proyecto portable entre máquinas.
**Dónde está en el código:** `backend/pyvenv.cfg` (el venv vive directamente en `backend/`, con `bin/activate`)

**Pregunta:** ¿Qué es un ORM?
**Respuesta:** Object-Relational Mapping: una capa que traduce clases y objetos de un lenguaje de programación a filas y tablas de una base de datos relacional, evitando escribir SQL directamente. Acá lo cumple SQLAlchemy.
**Dónde está en el código:** ver sección "Base de datos"

**Pregunta:** ¿Qué es REST y cómo se aplica acá?
**Respuesta:** Un estilo de arquitectura donde cada recurso tiene una URL y se opera sobre él con verbos HTTP (GET=leer, POST=crear, PUT=actualizar, DELETE=borrar). `flask-restful` estructura cada recurso como una clase con un método por verbo.
**Dónde está en el código:** `backend/main/resources/usuario.py` — la clase `Usuario` define `get`, `delete`, `put` (no hay `post` en el recurso singular, ese va en `Usuarios`)

**Pregunta:** ¿Qué roles tiene el sistema y qué puede hacer cada uno?
**Respuesta:** `admin` (control total: usuarios, cuotas, clases, precios), `profesor` (gestiona alumnos y planificaciones, puede suspender alumnos pero no crear cuotas ni borrar usuarios no-alumnos) y `user` (alumno: ve su perfil, su cuota, su planificación). El rol se valida server-side en cada endpoint sensible con `role_required`.
**Dónde está en el código:** `backend/main/models/usuario.py` línea 130 (`valid_roles = ["admin", "profesor", "user"]`) y `backend/main/resources/usuario.py` líneas 57-60 (ejemplo de restricción: un profesor solo puede borrar usuarios con rol `user`)

---

## Preguntas adicionales a repasar

**Pregunta:** ¿Diferencia entre `@Component`, `@NgModule`, `@Injectable`, `@Directive` y `@Pipe`?
**Respuesta:** `@Component` define una vista con su propio template/estilos. `@NgModule` agrupa componentes, servicios y otros módulos. `@Injectable` marca una clase como inyectable por el sistema de DI (típicamente servicios). `@Directive` agrega comportamiento a un elemento existente sin template propio. `@Pipe` transforma un valor dentro del template (`{{ valor | pipe }}`).
**Dónde está en el código:** el proyecto usa `@Component` (todos los `*.component.ts`), `@NgModule` (`app.module.ts`) e `@Injectable` (todos los `*.service.ts`). No encontré ningún `@Directive` ni `@Pipe` custom — solo se usa el `DatePipe` nativo de Angular, registrado como provider en `app.module.ts` línea 52.

**Pregunta:** ¿Diferencia entre `relationship()` y `ForeignKey()` en SQLAlchemy?
**Respuesta:** `ForeignKey` es la restricción real a nivel de columna y de base de datos (garantiza integridad referencial). `relationship` es un atributo a nivel de Python/ORM que permite navegar el objeto relacionado (`cuota.alumno`) sin escribir el JOIN, y no existe como columna en la tabla.
**Dónde está en el código:** `backend/main/models/cuota.py` líneas 12 y 21 (ver sección Base de datos)

**Pregunta:** ¿Qué pasa si el token expira? ¿Lo maneja algún interceptor?
**Respuesta:** No hay interceptor. El guard de rutas (`authsessionGuard`) revisa la expiración *antes* de entrar a una vista protegida y redirige a login/home si venció. Si el token vence en medio de una sesión activa (sin cambiar de ruta), el backend simplemente devolverá 401 en la próxima petición y ese error no está centralizado — cada `subscribe(...error...)` lo maneja por separado (ver `login.component.ts` líneas 51-59 como ejemplo del patrón de manejo de errores usado).
**Dónde está en el código:** `frontend/gol_gym/src/app/guards/authsession.guard.ts`

**Pregunta:** ¿Diferencia entre `localStorage` y `sessionStorage`?
**Respuesta:** `localStorage` persiste indefinidamente (sobrevive a cerrar el navegador) y es compartido entre pestañas del mismo origen. `sessionStorage` se borra al cerrar la pestaña y es exclusivo de esa pestaña. El proyecto usa `localStorage` para la sesión del usuario logueado, y `sessionStorage` puntualmente para no perder de vista qué perfil ajeno se estaba mirando tras un F5.
**Dónde está en el código:** `frontend/gol_gym/src/app/pages/vista-perfil/vista-perfil.component.ts` líneas 17-26 (usa ambos con prioridad `history.state` > `sessionStorage` > `localStorage`)

**Pregunta:** ¿Qué es CORS y usa este proyecto `flask-cors`?
**Respuesta:** CORS (Cross-Origin Resource Sharing) es el mecanismo del navegador que bloquea peticiones entre distintos orígenes (dominio/puerto) salvo que el servidor lo autorice explícitamente con headers. **Este proyecto no tiene `flask-cors` instalado** (no está en `requirements.txt`); en desarrollo evita el problema con `proxy.conf.json` de Angular, que reenvía `/api` al backend como si fueran el mismo origen. Para producción real haría falta agregar `flask-cors` — está listado como pendiente en `retomar.txt`.
**Dónde está en el código:** `backend/requirements.txt` (no aparece `flask-cors`) + `frontend/gol_gym/proxy.conf.json`

**Pregunta:** ¿Diferencia entre `Observable` y `Promise` en Angular?
**Respuesta:** Una `Promise` resuelve un solo valor una vez y no se puede cancelar. Un `Observable` (de RxJS) puede emitir múltiples valores en el tiempo, se puede cancelar (`unsubscribe`) y soporta operadores de transformación (`.pipe()`, `map`, `take`, etc). `HttpClient` de Angular devuelve `Observable` por eso.
**Dónde está en el código:** `frontend/gol_gym/src/app/services/auth.service.ts` línea 16 (`login(...): Observable<any> { return this.httpClient.post(...).pipe(take(1)); }`)

**Pregunta:** Ciclo de vida de un componente Angular — ¿cuáles conocés y en qué orden?
**Respuesta:** El más usado es `ngOnInit` (una vez, tras crear el componente e inicializar sus `@Input`). También existe `ngOnDestroy` (limpieza al sacar el componente del DOM). Otros del ciclo completo (no usados en este proyecto): `ngOnChanges`, `ngAfterViewInit`, `ngAfterContentInit`.
**Dónde está en el código:** `frontend/gol_gym/src/app/app.component.ts` líneas 8-19 (`OnInit` + `OnDestroy` con un timer que se limpia)

**Pregunta:** ¿Diferencia entre PUT y PATCH? ¿Cuál usa este proyecto?
**Respuesta:** `PUT` reemplaza el recurso completo (semánticamente), `PATCH` aplica una modificación parcial. **Este proyecto usa únicamente `PUT`** para todas las actualizaciones (incluso las parciales, como suspender un usuario o marcar una cuota como pagada) — no hay ningún endpoint `PATCH`.
**Dónde está en el código:** `backend/main/resources/usuario.py` línea 65 (`def put(self, dni):`) — el mismo método maneja tanto actualización de datos generales como de suspensión, según qué campos llegan en el body.

**Pregunta:** ¿Qué es una migración y por qué no crear las tablas a mano?
**Respuesta:** Ver sección Base de datos — script versionado e incremental que modifica el esquema sin perder datos, generado comparando el estado de los modelos contra la BD actual.
**Dónde está en el código:** `backend/migrations/versions/`

**Pregunta:** Se ve una inconsistencia entre backend y frontend en la validación de contraseña — ¿cuál es?
**Respuesta:** El modelo (`plain_password` setter) permite contraseñas de hasta 128 caracteres, pero los formularios reactivos del frontend (login y alta de usuario) todavía validan `Validators.maxLength(20)`. Es una desprolijidad real del código actual: el backend fue actualizado (commit `bb684cb`) pero los formularios del frontend no se tocaron. Si te preguntan "¿por qué el input no te deja poner una password larga si el backend la acepta?", la respuesta es esta.
**Dónde está en el código:** backend permite 128 en `backend/main/models/usuario.py` línea 47; frontend sigue en 20 en `frontend/gol_gym/src/app/pages/login/login.component.ts` línea 26 y `frontend/gol_gym/src/app/components/lista-usuarios/lista-usuarios.component.ts` línea 45.

**Pregunta:** ¿Cómo se envían los mails automáticos del sistema (cuotas, suspensión, bienvenida)?
**Respuesta:** Con `Flask-Mail`, configurado con credenciales SMTP de Gmail (App Password) vía variables de entorno. Cada evento de negocio (registro, primera cuota, cuota rechazada, cuota pagada, suspensión, activación) dispara un `sendMail(...)` con una plantilla distinta.
**Dónde está en el código:** `backend/main/__init__.py` líneas 93-102 (config de Mail) y `backend/main/auth/routes.py` línea 90 (ejemplo de llamada, mail "primera cuota")

---

*Generado y verificado contra el código real de `backend/` y `frontend/gol_gym/` — todas las referencias de línea corresponden al estado del repo al 28/07/2026. Si el código cambia, las líneas pueden desactualizarse; ante la duda, priorizá lo que ves en el editor por sobre esta guía.*
