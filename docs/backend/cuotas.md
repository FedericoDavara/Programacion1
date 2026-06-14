# Módulo de Cuotas / Suscripción

Implementado en la iteración 2 del proyecto. Gestiona el cobro mensual de membresías, el monitoreo de pagos y la suspensión automática de alumnos morosos.

---

## Modelo Cuota

**Archivo:** `backend/main/models/cuota.py`  
**Tabla:** `cuota`

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `id` | Integer PK | autoincrement | — |
| `alumno_dni` | Integer FK→Alumno | — | Alumno dueño de la cuota |
| `plan` | String(150) | — | Nombre del plan (Street Fighter) |
| `monto_base` | Float | — | Precio sin recargo |
| `recargo_porcentaje` | Float | 10.0 | % de recargo por mora |
| `fecha_emision` | DateTime | now() | Cuándo se generó |
| `fecha_vencimiento` | DateTime | — | Fecha límite de pago |
| `fecha_pago` | DateTime | NULL | Cuándo se pagó (null = no pagado) |
| `intentos_cobro` | Integer | 0 | Reintentos fallidos (máx 3) |

**Propiedades calculadas (no se guardan en DB):**

```python
cuota.estado       # calculado desde fechas e intentos_cobro
cuota.monto_total  # monto_base * 1.10 si está vencida sin pagar
```

### Lógica del estado

```
fecha_pago != null                          → AL_DIA
fecha_vencimiento > hoy + 3 días            → PENDIENTE
0 <= (fecha_vencimiento - hoy).days <= 3    → POR_VENCER
hoy > fecha_vencimiento AND intentos < 3    → RECHAZADO
hoy > fecha_vencimiento AND intentos >= 3   → VENCIDA
```

### Cambios en Alumno

Se agregaron dos campos nuevos a la tabla `alumno`:

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `estado_membresia` | String(20) | 'ACTIVO' | ACTIVO, MOROSO, SUSPENDIDO |
| `plan` | String(150) | NULL | Plan vigente del alumno |

---

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/cuotas` | admin/prof | Lista todas las cuotas con resumen |
| POST | `/cuotas` | admin | Crea una nueva cuota y envía email |
| GET | `/cuota/<id>` | JWT | Obtiene una cuota por id |
| PUT | `/cuota/<id>/pagar` | admin | Registra el pago y envía confirmación |
| DELETE | `/cuota/<id>` | admin | Elimina una cuota |
| GET | `/cuotas_alumno/<dni>` | JWT | Cuotas de un alumno específico |
| POST | `/cuotas/procesar_vencimientos` | admin | Procesa mora y suspensiones |

### GET /cuotas — query params opcionales

| Param | Descripción |
|-------|-------------|
| `estado` | Filtra por estado: AL_DIA, POR_VENCER, RECHAZADO, VENCIDA, PENDIENTE |
| `alumno_dni` | Filtra por DNI del alumno |

**Respuesta:**
```json
{
  "cuotas": [
    {
      "id": 1,
      "alumno_dni": 1234567,
      "nombre": "Juan",
      "apellido": "Perez",
      "email": "juan@mail.com",
      "plan": "Street Fighter II (The World Warrior)",
      "monto_base": 22000.0,
      "monto_total": 22000.0,
      "recargo_porcentaje": 10.0,
      "fecha_vencimiento": "2026-07-14T00:00:00",
      "fecha_pago": null,
      "intentos_cobro": 0,
      "estado": "PENDIENTE"
    }
  ],
  "resumen": {
    "total": 10,
    "al_dia": 5,
    "por_vencer": 2,
    "rechazado": 1,
    "vencidas": 2,
    "pendientes": 0
  }
}
```

---

## Flujo de cobro

```
1. Alumno se registra (POST /auth/register)
   ↓
2. Backend crea Cuota automáticamente:
   - plan = plan elegido (default: Street Fighter II)
   - monto_base = monto del plan
   - fecha_vencimiento = hoy + 30 días
   ↓
3. Se envía email "primera_cuota" al alumno

4. Admin ve tabla de Socios (/cuotas) → ve estado de cada cuota
   ↓
5. Admin registra pago → PUT /cuota/{id}/pagar
   - fecha_pago = ahora
   - alumno.estado_membresia = 'ACTIVO'
   - Si estaba suspendido → se reactiva
   - Email "cuota_pagada" → PLAYER 1 READY ✅

6. Si no paga → POST /cuotas/procesar_vencimientos (manual o cron)
   - intentos_cobro += 1
   - Si intentos < 3:
     - alumno.estado_membresia = 'MOROSO'
     - Email "cuota_rechazada" → GAME OVER (por ahora)
   - Si intentos >= 3:
     - alumno.estado_membresia = 'SUSPENDIDO'
     - usuario.fecha_suspension = ahora + 365 días
     - usuario.motivo_suspension = "Cuota impaga"
     - Email "suspension" → PLAYER BLOCKED 🔴
```

---

## Templates de email

| Template | Asunto | Cuándo |
|----------|--------|--------|
| `primera_cuota` | 🪙 INSERT COIN — Tu primera cuota en GOL GYM | Al registrarse |
| `cuota_por_vencer` | ⚠️ CONTINUE? X... — Tu cuota vence pronto | Al detectar POR_VENCER |
| `cuota_rechazada` | 💀 GAME OVER (por ahora) | Cada intento fallido |
| `cuota_pagada` | ✅ PLAYER 1 READY — Membresía activa | Al registrar pago |
| `suspension` (existente) | 🔴 PLAYER BLOCKED | Al suspender por mora |

---

## Planes (tabla Precios)

Los 5 planes se cargan con `backend/seed_planes.py`:

| ID | Plan | Precio |
|----|------|--------|
| 1 | Street Fighter II (The World Warrior) | $22.000 ARS |
| 2 | Street Fighter II Turbo (Hyper Fighting) | $28.000 ARS |
| 3 | Super Street Fighter II Turbo (The Ultimate Championship) | $35.000 ARS |
| 4 | Ultra Street Fighter IV (Arcade Edition) | $42.000 ARS |
| 5 | Super Street Fighter II: The New Challengers | $24.000 ARS por persona |

---

## Frases temáticas en notificaciones

| Situación | Frase |
|-----------|-------|
| Cuota pendiente | `🪙 INSERT COIN` |
| Cuota pagada | `✅ PLAYER 1 READY` |
| Por vencer | `⚠️ CONTINUE? X... 2... 1...` |
| Vencida | `💀 GAME OVER (por ahora)` |
| Suspensión | `🔴 PLAYER BLOCKED` |
| Reactivación | `🟢 REMATCH!` |
| Registro | `🎮 NEW CHALLENGER APPROACHING` |
