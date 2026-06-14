# Routing y Guards

**Archivos:**
- `frontend/gol_gym/src/app/app-routing.module.ts`
- `frontend/gol_gym/src/app/guards/authsession.guard.ts`

---

## Tabla de rutas

| Ruta | Componente | Guard | Acceso |
|------|-----------|-------|--------|
| `/home` | HomeComponent | — | Público |
| `/login` | LoginComponent | — | Público |
| `/vInicio` | VistaInicioComponent | `authsessionGuard` | Privado (admin/profesor) |
| `/vPerfil` | VistaPerfilComponent | `authsessionGuard` | Privado (cualquier rol) |
| `/vPlanif` | VistaPlanificacionComponent | `authsessionGuard` | Privado (cualquier rol) |
| `/vError` | VistaErrorComponent | — | Público (error/suspensión) |
| `` (vacía) | — | — | Redirige a `/home` |
| `**` (wildcard) | — | — | Redirige a `/vError` |

---

## Guard: authsessionGuard

**Archivo:** `guards/authsession.guard.ts`  
**Tipo:** `CanActivateFn` (functional guard, patrón de Angular 15+)

```typescript
export const authsessionGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('token');
  
  if (!token) {
    router.navigate(['/home']);
    return false;
  }
  return true;
};
```

**Lo que hace:** verifica que exista la clave `token` en `localStorage`.  
**Lo que NO hace:**
- No valida si el token está expirado
- No valida la firma del JWT
- No verifica el rol del usuario logueado

**Consecuencia:** si el token existe pero ya expiró, el guard deja pasar al usuario pero el backend rechazará los requests con 401.

---

## Navegación entre componentes

Angular Router usa `history.state` para pasar datos entre rutas sin exponerlos en la URL:

```typescript
// Navegar al perfil de un usuario específico
this.router.navigate(['/vPerfil'], { state: { dni: 1234567 } });

// En el componente destino
const dni = history.state.dni;
```

Este patrón se usa en:
- `ListaUsuariosComponent` → `PerfilComponent` (pasa `dni`)
- `PerfilComponent` → `PlanificacionComponent` (pasa `dni`)

**Limitación:** si el usuario refresca la página en `/vPerfil`, `history.state.dni` se pierde y el componente no sabe qué usuario mostrar. En ese caso, el componente debería usar el DNI del token (`UsuariosService.getUserDNIFromToken()`).

---

## Módulo principal

**Archivo:** `app.module.ts`

```typescript
@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    VistaInicioComponent,
    VistaPerfilComponent,
    VistaPlanificacionComponent,
    VistaErrorComponent,
    NavbarComponent,
    NavcloseComponent,
    PerfilComponent,
    PlanificacionComponent,
    ListaUsuariosComponent,
    ListaClasesComponent,
    ListaProfesoresComponent,
    ListaPreciosComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
```

No hay providers de servicios declarados explícitamente porque los servicios usan `providedIn: 'root'` (singleton a nivel de aplicación).

No hay interceptores HTTP registrados.
