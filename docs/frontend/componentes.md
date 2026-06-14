# Componentes Angular

**Ruta base:** `frontend/gol_gym/src/app/`  
Framework: Angular 16, sin librería de UI externa (CSS3 puro).

---

## Páginas (pages/)

### HomeComponent
**Archivo:** `pages/home/home.component.ts`  
**Ruta:** `/home` (pública)

Vista principal del gimnasio. Es la landing page.

**Datos que carga:**
- Clases disponibles (via ClasesService → GET /clases)
- Precios/planes (via PreciosService → GET /precios)
- Profesores (via UsuariosService → GET /usuarios_p)

**Funcionalidades:**
- Ordena las clases por día de la semana y horario antes de mostrarlas.
- Sección de contacto con `FormGroup` validado:
  - `nombre`: requerido
  - `email`: formato válido
  - `mensaje`: requerido
  - Envía a `ContactoService.enviarMensaje()` → POST /contacto (**endpoint no implementado en backend**)
- Scroll suave a la sección de clases.
- Muestra cards de profesores con foto y descripción.

---

### LoginComponent
**Archivo:** `pages/login/login.component.ts`  
**Ruta:** `/login` (pública)

Formulario de autenticación.

**FormGroup:**
- `email`: validadores de formato, valor default `cr7@gmail.com`
- `password`: 6-20 caracteres, valor default `madrid15`

**Flujo tras login exitoso:**
1. Llama `AuthService.login()`
2. Decodifica el JWT con `jwt-decode` para extraer el rol
3. Si `rol == 'admin'` o `'profesor'` → navega a `/vInicio`
4. Si `rol == 'user'` → navega a `/vPerfil`

**Manejo de suspensión:**
- Si el backend retorna 403 → redirige a `/vError?suspended=true&fecha=...&motivo=...`

---

### VistaInicioComponent
**Archivo:** `pages/vista-inicio/vista-inicio.component.ts`  
**Ruta:** `/vInicio` (protegida por `authsessionGuard`)

Vista de panel de control para admin y profesores. Actúa como contenedor/layout que incluye:
- `NavbarComponent`
- `ListaUsuariosComponent`
- `ListaClasesComponent`
- `ListaProfesoresComponent`
- `ListaPreciosComponent`

---

### VistaPerfilComponent
**Archivo:** `pages/vista-perfil/vista-perfil.component.ts`  
**Ruta:** `/vPerfil` (protegida por `authsessionGuard`)

Contenedor para la vista de perfil del alumno. Incluye `PerfilComponent` con el DNI del usuario logueado.

---

### VistaPlanificacionComponent
**Archivo:** `pages/vista-planificacion/vista-planificacion.component.ts`  
**Ruta:** `/vPlanif` (protegida por `authsessionGuard`)

Contenedor para la vista de planificación. Incluye `PlanificacionComponent` con el DNI recibido via `history.state`.

---

### VistaErrorComponent
**Archivo:** `pages/vista-error/vista-error.component.ts`  
**Ruta:** `/vError` (pública)

Pantalla de error genérica. Detecta si viene de una suspensión via `ActivatedRoute.queryParams`:
- Si `suspended=true`: muestra fecha y motivo de la suspensión.
- Botón "Salir": limpia `localStorage` y redirige a `/`.

---

## Componentes reutilizables (components/)

### PerfilComponent
**Archivo:** `components/perfil/perfil.component.ts`

Muestra y edita el perfil de un usuario. Recibe el DNI via `history.state.dni`.

**Formulario dinámico:** los campos y validadores cambian según el rol:

*Para alumno (`rol='user'`):*
- `edad`: 13-100, entero positivo
- `peso`: 40-200, permite coma/punto decimal
- `altura`: 1.40-2.20, permite coma/punto decimal
- `sexo`: dropdown Masculino/Femenino

*Para profesor:*
- `especialidad`: 3-50 chars, solo letras

**Validators custom:**
- `pesoRangoValidator`: rechaza fuera de 40-200
- `alturaRangoValidator`: rechaza fuera de 1.40-2.20
- `edadEnteraPositivaValidator`: debe ser entero positivo

**Flujo:**
1. Carga usuario con `GET /usuario/{dni}`
2. Si tiene sub-registro: pre-llena el formulario
3. Si no tiene sub-registro (usuario sin perfil completo): muestra formulario vacío para crear
4. Al guardar: actualiza Usuario base + crea/actualiza Alumno o Profesor
5. Botón "Ver Planificación": navega a `/vPlanif` con `state.dni` (solo si el alumno ya tiene todos sus datos)
6. Botón "Eliminar usuario": DELETE + navega atrás

---

### PlanificacionComponent
**Archivo:** `components/planificacion/planificacion.component.ts`

Formulario de planificación semanal. Recibe DNI del alumno via `history.state`.

**Campos del formulario:**
- `descripcion`: 3-200 chars, requerida
- `fecha`: requerida
- `lunes`, `martes`, `miercoles`, `jueves`, `viernes`, `sabado`: opcionales, max 1000 chars cada uno
- `profesor_dni`: dropdown que carga desde GET /usuarios_p

**Flujo:**
1. Carga profesores disponibles para el dropdown
2. Llama `PlanificacionService.getPlanif(dni)` → GET /planificacion_a/{dni}
3. Si hay planificación existente: pre-llena el formulario (modo edición)
4. Si no existe: modo creación
5. Al guardar: POST o PUT según corresponda (convierte `profesor_dni` a número)
6. Botón "Eliminar": DELETE /planificacion/{id}

---

### ListaUsuariosComponent
**Archivo:** `components/lista-usuarios/lista-usuarios.component.ts`

Tabla de gestión de usuarios con todas las operaciones CRUD.

**Funcionalidades:**
- Paginación de 10 usuarios por página
- Búsqueda en tiempo real (activa con ≥3 caracteres)
- Filtro por rol
- Crear usuario con formulario modal (campos dinámicos según rol elegido)
- Editar usuario (nombre, apellido, email, teléfono, especialidad si es profesor, password opcional)
- Suspender usuario: pide fecha y motivo → PUT /usuario/{dni} con `fecha_suspension`
- Activar usuario: limpia `fecha_suspension` → PUT /usuario/{dni} con `fecha_suspension: null`
- Botón "Ver Perfil": navega a `/vPerfil` via `history.state.dni`
- Indicador visual de usuarios suspendidos

**Restricciones según rol del logueado:**
- `profesor` logueado: solo ve y gestiona usuarios con `rol='user'`
- `admin` logueado: ve y gestiona todos

---

### ListaClasesComponent
**Archivo:** `components/lista-clases/lista-clases.component.ts`

Tabla de gestión de clases del gimnasio (solo admin).

**Formulario (crear/editar):**
- `nombre`: 3-50 chars
- `dia`: dropdown (Lunes, Martes, Miércoles, Jueves, Viernes, Sábado)
- `horario`: regex `HH:MM` o `HH:MM-HH:MM`
- `imagen`: URL opcional

**Operaciones:** Crear, editar, eliminar.

---

### ListaProfesoresComponent
**Archivo:** `components/lista-profesores/lista-profesores.component.ts`

Vista de la lista de profesores con capacidad de edición (solo admin).

**Campos editables:** `foto` (URL), `descripcion` (3-250 chars)  
Los campos de nombre, apellido y especialidad se editan desde `ListaUsuariosComponent`.

---

### ListaPreciosComponent
**Archivo:** `components/lista-precios/lista-precios.component.ts`

Tabla de gestión de planes y precios (solo admin).

**Formulario:** `nombre`, `precio` (string libre), `descripcion` (opcional)  
**Operaciones:** Crear, editar, eliminar.

---

### NavbarComponent / NavcloseComponent
Barra de navegación con links contextuales según el rol almacenado en `localStorage`.  
Botón de logout que limpia `localStorage` y redirige a `/home`.

---

### AppComponent
**Archivo:** `app.component.ts`

Componente raíz. Contiene un banner/alerta que:
- Se muestra al iniciar
- Desaparece automáticamente en 5 segundos
- Pausa el timer si el cursor está encima (hover)
