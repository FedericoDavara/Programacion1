# Datos Semilla

El proyecto incluye dos scripts de seed en `backend/`:

| Script | Propósito |
|--------|-----------|
| `seed_data.py` | Carga completa: usuarios, alumnos, profesores, clases, planificaciones, cuotas y precios |
| `seed_planes.py` | Solo repuebla los 5 planes Street Fighter (no toca usuarios ni cuotas) |

---

## seed_data.py

Uso:
```bash
cd backend
python3 seed_data.py
```

### Estrategia

- **Conserva** los permisos existentes (`permiso`) — son config del sistema.
- **Borra y recrea** el resto: `usuario`, `alumno`, `profesor`, `clase`, `planificacion`, `cuota`, `precio`.
- Si faltan permisos de cuotas (los 6 de admin/profesor), los agrega sin duplicar.

### Usuarios creados

| Rol | Email | Password | Notas |
|-----|-------|----------|-------|
| admin | `gimenezbenja2@gmail.com` | `Admin1234` | Correo real — recibe emails del gym |
| admin | `admin2@golgym.com` | `Admin1234` | — |
| admin | `cr7@gmail.com` | `madrid15` | Usuario histórico del proyecto |
| profesor | `lionel.messi@golgym.com` | `Profe1234` | Especialidad: Cardio |
| profesor | `mike.tyson@golgym.com` | `Profe1234` | Especialidad: Boxeo |
| profesor | `michael.jordan@golgym.com` | `Profe1234` | Especialidad: Musculación |
| alumno | `fliagimenez2026@gmail.com` | `Alumno1234` | **Correo real** — cuota POR_VENCER |
| alumno | `hernestolopez2026@gmail.com` | `Alumno1234` | **Correo real** — cuota VENCIDA / SUSPENDIDO |
| alumno | `valentina.lopez@golgym.com` | `Alumno1234` | Cuota AL_DIA |
| alumno | `matias.ruiz@golgym.com` | `Alumno1234` | Cuota AL_DIA |
| alumno | `camila.torres@golgym.com` | `Alumno1234` | Cuota PENDIENTE |
| alumno | `joaquin.morales@golgym.com` | `Alumno1234` | Cuota RECHAZADA / MOROSO |

### Estados de cuota por alumno

Cada alumno tiene una cuota en un estado distinto para facilitar las pruebas:

| Estado | Cómo se genera | Alumno de ejemplo |
|--------|---------------|-------------------|
| `AL_DIA` | `fecha_vencimiento = hoy - 5d`, `fecha_pago = hoy` | Valentina Lopez |
| `PENDIENTE` | `fecha_vencimiento = hoy + 20d` | Camila Torres |
| `POR_VENCER` | `fecha_vencimiento = hoy + 2d` | Flia Gimenez |
| `RECHAZADO` | `fecha_vencimiento = hoy - 1d`, `intentos_cobro = 1` | Joaquin Morales |
| `VENCIDA` | `fecha_vencimiento = hoy - 4d`, `intentos_cobro = 3` | Hernesto Lopez |

> Los estados son calculados en Python (`@property` en `Cuota`) — no se almacenan en la base de datos. Ver [cuotas.md](cuotas.md) para más detalle.

### Clases creadas

7 clases distribuidas de lunes a sábado, con sus profesores asignados vía la tabla `procla` (relación M:N).

### Planificaciones creadas

6 planificaciones — una por alumno — con rutinas detalladas por día de la semana.

---

## seed_planes.py

Uso:
```bash
cd backend
python3 seed_planes.py
```

Borra todos los `Precio` existentes e inserta los 5 planes Street Fighter:

| Plan | Precio |
|------|--------|
| Street Fighter II (The World Warrior) | $22.000 ARS |
| Street Fighter II Turbo (Hyper Fighting) | $28.000 ARS |
| Super Street Fighter II: The New Challengers | $24.000 ARS por persona |
| Super Street Fighter II Turbo (The Ultimate Championship) | $35.000 ARS |
| Ultra Street Fighter IV (Arcade Edition) | $42.000 ARS |

---

## Correos reales de prueba

Los correos reales están listados en `correos.md` (excluido del repo via `.gitignore`).
Al correr el seed, los alumnos con correos reales recibirán emails transaccionales reales cuando se usen los endpoints de cuotas (pago, vencimiento, rechazo).
