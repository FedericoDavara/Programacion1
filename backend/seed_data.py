"""
Datos semilla para GOL GYM.

Estrategia:
  - Conserva los permisos existentes (son config del sistema).
  - Limpia usuarios, alumnos, profesores, clases, planificaciones y cuotas.
  - Recrea todo con datos coherentes con el sistema actual.
  - Los correos reales (correos.md) quedan asignados a usuarios que
    recibirán los emails de prueba reales.

Correos reales disponibles:
  gimenezbenja2@gmail.com   → Admin principal (recibe todo)
  fliagimenez2026@gmail.com → Alumno con cuota POR_VENCER
  hernestolopez2026@gmail.com → Alumno con cuota VENCIDA (para probar suspensión)

Uso: python3 seed_data.py
"""

from app import app
from main import db
from main.models import (
    UsuarioModel, AlumnoModel, ProfesorModel,
    ClaseModel, PlanificacionModel, CuotaModel,
    PermisoModel, PrecioModel,
)
from datetime import datetime, timedelta, timezone

# ── helpers ──────────────────────────────────────────────────────────────────

def hoy():
    return datetime.now(timezone.utc).replace(tzinfo=None)

def fecha(dias_desde_hoy: int) -> datetime:
    return hoy() + timedelta(days=dias_desde_hoy)


# ── datos ────────────────────────────────────────────────────────────────────

PLANES = {
    "sf2":      "Street Fighter II (The World Warrior)",
    "sf2turbo": "Street Fighter II Turbo (Hyper Fighting)",
    "ssf2":     "Super Street Fighter II Turbo (The Ultimate Championship)",
    "usf4":     "Ultra Street Fighter IV (Arcade Edition)",
    "group":    "Super Street Fighter II: The New Challengers",
}

PRECIOS_SF = [
    {"nombre": PLANES["sf2"],      "precio": "$22.000 ARS", "descripcion": "El clásico que lo empezó todo. Musculación 2-3 veces/semana. 🥋"},
    {"nombre": PLANES["sf2turbo"], "precio": "$28.000 ARS", "descripcion": "Pusiste el turbo. Pase libre + clases seleccionadas. ⚡"},
    {"nombre": PLANES["ssf2"],     "precio": "$35.000 ARS", "descripcion": "El nombre más largo para el plan más completo. Todo incluido + casillero. 🔥"},
    {"nombre": PLANES["usf4"],     "precio": "$42.000 ARS", "descripcion": "Para los que van en serio. Rutina personalizada + beneficios en suplementos. 👑"},
    {"nombre": PLANES["group"],    "precio": "$24.000 ARS por persona", "descripcion": "Modo cooperativo. Plan grupal para amigos, parejas o familia. 👥"},
]

USUARIOS = [
    # ── ADMIN ──────────────────────────────────────────────────────────────
    {
        "dni": 9000001, "nombre": "Victor", "apellido": "Gimenez",
        "email": "gimenezbenja2@gmail.com",   # ← correo real
        "password": "Admin1234", "telefono": 1155667788, "rol": "admin",
    },
    {
        "dni": 9000002, "nombre": "Federico", "apellido": "Davara",
        "email": "admin2@golgym.com",
        "password": "Admin1234", "telefono": 1144556677, "rol": "admin",
    },
    {
        "dni": 9000003, "nombre": "Cristiano", "apellido": "Ronaldo",
        "email": "cr7@gmail.com",
        "password": "madrid15", "telefono": 1100000007, "rol": "admin",
    },

    # ── PROFESORES ─────────────────────────────────────────────────────────
    {
        "dni": 1000001, "nombre": "Lionel", "apellido": "Messi",
        "email": "lionel.messi@golgym.com",
        "password": "Profe1234", "telefono": 2614001001, "rol": "profesor",
        "especialidad": "Cardio",
        "foto": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg",
        "descripcion": "10 balones de oro, infinitas sentadillas. El mejor en la cancha y en el gym.",
    },
    {
        "dni": 1000002, "nombre": "Mike", "apellido": "Tyson",
        "email": "mike.tyson@golgym.com",
        "password": "Profe1234", "telefono": 2614001002, "rol": "profesor",
        "especialidad": "Boxeo",
        "foto": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Mike_Tyson_2019_by_Glenn_Francis.jpg",
        "descripcion": "Todo el mundo tiene un plan hasta que te pegan una trompada. Ex campeón mundial, ahora profe de boxeo.",
    },
    {
        "dni": 1000003, "nombre": "Michael", "apellido": "Jordan",
        "email": "michael.jordan@golgym.com",
        "password": "Profe1234", "telefono": 2614001003, "rol": "profesor",
        "especialidad": "Musculacion",
        "foto": "https://upload.wikimedia.org/wikipedia/commons/a/ae/Michael_Jordan_in_2014.jpg",
        "descripcion": "Seis campeonatos, seis MVPs. Ahora te enseña a ser el MVP de tu propia rutina.",
    },

    # ── ALUMNOS ────────────────────────────────────────────────────────────
    # correos reales primero
    {
        "dni": 4000001, "nombre": "Flia", "apellido": "Gimenez",
        "email": "fliagimenez2026@gmail.com",   # ← correo real
        "password": "Alumno1234", "telefono": 1155001001, "rol": "user",
        "edad": 30, "peso": 75, "altura": 1.75, "sexo": "Masculino",
        "plan": PLANES["sf2turbo"], "monto": 28000,
        "estado_cuota": "POR_VENCER",   # vence en 2 días → recibirá el aviso
    },
    {
        "dni": 4000002, "nombre": "Hernesto", "apellido": "Lopez",
        "email": "hernestolopez2026@gmail.com",   # ← correo real
        "password": "Alumno1234", "telefono": 1155002002, "rol": "user",
        "edad": 25, "peso": 82, "altura": 1.80, "sexo": "Masculino",
        "plan": PLANES["usf4"], "monto": 42000,
        "estado_cuota": "VENCIDA",   # venció hace 4 días → moroso
    },
    # alumnos ficticios
    {
        "dni": 4000003, "nombre": "Valentina", "apellido": "Lopez",
        "email": "valentina.lopez@golgym.com",
        "password": "Alumno1234", "telefono": 1155003003, "rol": "user",
        "edad": 22, "peso": 58, "altura": 1.65, "sexo": "Femenino",
        "plan": PLANES["ssf2"], "monto": 35000,
        "estado_cuota": "AL_DIA",
    },
    {
        "dni": 4000004, "nombre": "Matias", "apellido": "Ruiz",
        "email": "matias.ruiz@golgym.com",
        "password": "Alumno1234", "telefono": 1155004004, "rol": "user",
        "edad": 28, "peso": 90, "altura": 1.82, "sexo": "Masculino",
        "plan": PLANES["sf2"], "monto": 22000,
        "estado_cuota": "AL_DIA",
    },
    {
        "dni": 4000005, "nombre": "Camila", "apellido": "Torres",
        "email": "camila.torres@golgym.com",
        "password": "Alumno1234", "telefono": 1155005005, "rol": "user",
        "edad": 19, "peso": 55, "altura": 1.60, "sexo": "Femenino",
        "plan": PLANES["group"], "monto": 24000,
        "estado_cuota": "PENDIENTE",   # vence en 20 días
    },
    {
        "dni": 4000006, "nombre": "Joaquin", "apellido": "Morales",
        "email": "joaquin.morales@golgym.com",
        "password": "Alumno1234", "telefono": 1155006006, "rol": "user",
        "edad": 33, "peso": 78, "altura": 1.78, "sexo": "Masculino",
        "plan": PLANES["sf2turbo"], "monto": 28000,
        "estado_cuota": "RECHAZADO",   # venció hace 1 día → primer reintento
    },
]

CLASES = [
    {"nombre": "Spinning",        "dia": "lunes",      "horario": "08:00-09:00",  "profesores": [1000001]},
    {"nombre": "Musculacion",     "dia": "lunes",      "horario": "17:00-22:00",  "profesores": [1000003]},
    {"nombre": "Boxeo",           "dia": "martes",     "horario": "18:00-20:00",  "profesores": [1000002]},
    {"nombre": "Cardio Intenso",  "dia": "miércoles",  "horario": "07:00-08:30",  "profesores": [1000001]},
    {"nombre": "Musculacion",     "dia": "jueves",     "horario": "17:00-22:00",  "profesores": [1000003]},
    {"nombre": "Crossfit",        "dia": "viernes",    "horario": "19:00-20:30",  "profesores": [1000001, 1000003]},
    {"nombre": "Boxeo Avanzado",  "dia": "sábado",     "horario": "10:00-12:00",  "profesores": [1000002]},
]

# planificaciones: (alumno_dni, profesor_dni, descripcion, rutinas por día)
PLANIFICACIONES = [
    (4000001, 1000001, "Rutina cardio para mejorar resistencia",
     {"lunes": "Cinta 30min + bici 20min", "miercoles": "Elíptica 40min + salto de soga 15min", "viernes": "Natación 45min"}),
    (4000002, 1000002, "Plan de boxeo funcional para fuerza y velocidad",
     {"martes": "Sombra 3x3min + bolsa 5x3min", "jueves": "Guantes con sparring 4x3min", "sabado": "Cardio boxístico 30min"}),
    (4000003, 1000003, "Hipertrofia tren superior",
     {"lunes": "Press banca 4x8 + remo 4x10", "miercoles": "Hombros 3x12 + bíceps 3x15", "viernes": "Fondos 4x10 + jalones 4x12"}),
    (4000004, 1000003, "Volumen general principiante",
     {"lunes": "Sentadilla 3x10 + prensa 3x12", "miercoles": "Peso muerto 3x8 + curl 3x12", "viernes": "Full body máquinas 3x15"}),
    (4000005, 1000001, "Mantenimiento y bienestar",
     {"lunes": "Caminata rápida 30min", "jueves": "Yoga + elongación 45min", "sabado": "Bici suave 30min"}),
    (4000006, 1000002, "Acondicionamiento físico + boxeo base",
     {"martes": "Cuerda + flexiones 3x20", "jueves": "Bolsa liviana 4x2min + abdominales", "sabado": "Circuito funcional 30min"}),
]


# ── estado de cuota → fechas ──────────────────────────────────────────────────

def cuota_fechas(estado: str):
    """Devuelve (fecha_vencimiento, fecha_pago, intentos) según el estado deseado."""
    if estado == "AL_DIA":
        return fecha(-5), hoy(), 0          # venció hace 5 días pero está pagada
    if estado == "PENDIENTE":
        return fecha(20), None, 0           # vence en 20 días
    if estado == "POR_VENCER":
        return fecha(2), None, 0            # vence en 2 días
    if estado == "RECHAZADO":
        return fecha(-1), None, 1           # venció ayer, 1 intento fallido
    if estado == "VENCIDA":
        return fecha(-4), None, 3           # venció hace 4 días, 3 intentos → suspendido
    return fecha(30), None, 0


# ── ejecución ─────────────────────────────────────────────────────────────────

with app.app_context():
    print("🗑️  Limpiando datos anteriores (se conservan permisos)...")

    db.session.query(CuotaModel).delete()
    db.session.query(PlanificacionModel).delete()
    # limpiar relación M:N clase-profesor
    db.session.execute(db.text("DELETE FROM procla"))
    db.session.query(ClaseModel).delete()
    db.session.query(AlumnoModel).delete()
    db.session.query(ProfesorModel).delete()
    db.session.query(UsuarioModel).delete()
    db.session.query(PrecioModel).delete()
    db.session.commit()
    print("   ✓ Tablas limpias\n")

    # ── Precios / Planes ──────────────────────────────────────────────────
    print("💰 Cargando planes Street Fighter...")
    for p in PRECIOS_SF:
        db.session.add(PrecioModel(nombre=p["nombre"], precio=p["precio"], descripcion=p["descripcion"]))
    db.session.commit()
    print(f"   ✓ {len(PRECIOS_SF)} planes cargados\n")

    # ── Usuarios ─────────────────────────────────────────────────────────
    print("👤 Creando usuarios...")
    for u in USUARIOS:
        usuario = UsuarioModel(
            dni=u["dni"], nombre=u["nombre"], apellido=u["apellido"],
            email=u["email"], telefono=u["telefono"], rol=u["rol"],
        )
        usuario.plain_password = u["password"]
        db.session.add(usuario)
        db.session.flush()   # para poder usar el dni antes del commit

        if u["rol"] == "profesor":
            prof = ProfesorModel(
                dni=u["dni"],
                especialidad=u["especialidad"],
                foto=u.get("foto"),
                descripcion=u.get("descripcion"),
            )
            db.session.add(prof)

        elif u["rol"] == "user":
            alumno = AlumnoModel(
                dni=u["dni"], edad=u["edad"], peso=u["peso"],
                altura=u["altura"], sexo=u["sexo"],
                plan=u["plan"], estado_membresia="ACTIVO",
            )
            db.session.add(alumno)
            db.session.flush()

            # Cuota con el estado correcto
            venc, pagada, intentos = cuota_fechas(u["estado_cuota"])
            cuota = CuotaModel(
                alumno_dni=u["dni"],
                plan=u["plan"],
                monto_base=float(u["monto"]),
                recargo_porcentaje=10.0,
                fecha_emision=fecha(-30),
                fecha_vencimiento=venc,
                fecha_pago=pagada,
                intentos_cobro=intentos,
            )
            db.session.add(cuota)

            # Si está VENCIDA, el alumno se suspende
            if u["estado_cuota"] == "VENCIDA":
                alumno.estado_membresia = "SUSPENDIDO"
                usuario.fecha_suspension = hoy() + timedelta(days=365)
                usuario.motivo_suspension = "Cuota impaga — sin pago luego de 3 intentos"
            elif u["estado_cuota"] == "RECHAZADO":
                alumno.estado_membresia = "MOROSO"

        print(f"   ✓ {u['rol'].upper():<9} {u['nombre']} {u['apellido']} — {u['email']}")

    db.session.commit()
    print()

    # ── Clases ───────────────────────────────────────────────────────────
    # La relación M:N se maneja desde Profesor.clases (secondary=procla)
    print("🏋️  Creando clases...")
    for c in CLASES:
        clase = ClaseModel(nombre=c["nombre"], dia=c["dia"], horario=c["horario"])
        db.session.add(clase)
        db.session.flush()
        for prof_dni in c["profesores"]:
            prof = db.session.get(ProfesorModel, prof_dni)
            if prof and clase not in prof.clases:
                prof.clases.append(clase)
        print(f"   ✓ {c['nombre']} — {c['dia']} {c['horario']}")
    db.session.commit()
    print()

    # ── Planificaciones ───────────────────────────────────────────────────
    print("📋 Creando planificaciones...")
    for alumno_dni, prof_dni, desc, dias in PLANIFICACIONES:
        plan = PlanificacionModel(
            alumno_dni=alumno_dni,
            profesor_dni=prof_dni,
            descripcion=desc,
            fecha=hoy(),
            lunes=dias.get("lunes"),
            martes=dias.get("martes"),
            miercoles=dias.get("miercoles"),
            jueves=dias.get("jueves"),
            viernes=dias.get("viernes"),
            sabado=dias.get("sabado"),
        )
        db.session.add(plan)
    db.session.commit()
    print(f"   ✓ {len(PLANIFICACIONES)} planificaciones creadas\n")

    # ── Permisos de cuotas (si faltan) ────────────────────────────────────
    print("🔐 Verificando permisos de cuotas...")
    permisos_cuota = [
        ("admin",   "cuotas",               "GET"),
        ("profesor","cuotas",               "GET"),
        ("admin",   "cuotas",               "POST"),
        ("admin",   "cuota",                "DELETE"),
        ("admin",   "cuotapagar",           "PUT"),
        ("admin",   "procesarvencimientos", "POST"),
    ]
    existentes = {(p.rol, p.recurso, p.metodo) for p in db.session.query(PermisoModel).all()}
    agregados = 0
    for rol, recurso, metodo in permisos_cuota:
        if (rol, recurso, metodo) not in existentes:
            db.session.add(PermisoModel(rol=rol, recurso=recurso, metodo=metodo))
            agregados += 1
    db.session.commit()
    print(f"   ✓ {agregados} permisos nuevos de cuota agregados\n")

    # ── Resumen final ─────────────────────────────────────────────────────
    print("=" * 55)
    print("✅ SEED COMPLETADO")
    print("=" * 55)

    from sqlalchemy import text
    for tabla in ["usuario", "alumno", "profesor", "clase", "planificacion", "cuota", "precio", "permiso"]:
        n = db.session.execute(text(f'SELECT COUNT(*) FROM "{tabla}"')).scalar()
        print(f"   {tabla:<18} {n} filas")

    print()
    print("🔑 ACCESOS DE PRUEBA:")
    print("   ADMIN   → gimenezbenja2@gmail.com  / Admin1234")
    print("   ADMIN   → admin2@golgym.com        / Admin1234")
    print("   PROFE   → lionel.messi@golgym.com  / Profe1234")
    print("   PROFE   → mike.tyson@golgym.com    / Profe1234")
    print("   PROFE   → michael.jordan@golgym.com/ Profe1234")
    print("   ALUMNO  → fliagimenez2026@gmail.com/ Alumno1234  (cuota POR VENCER)")
    print("   ALUMNO  → hernestolopez2026@gmail.com/ Alumno1234 (VENCIDA/SUSPENDIDO)")
    print("   ALUMNO  → valentina.lopez@golgym.com/ Alumno1234 (AL DIA)")
    print("   ALUMNO  → joaquin.morales@golgym.com/ Alumno1234  (RECHAZADO/MOROSO)")
    print()
    print("📧 CORREOS REALES QUE RECIBIRÁN EMAILS:")
    print("   gimenezbenja2@gmail.com     ← admin, recibe emails de contacto y gestión")
    print("   fliagimenez2026@gmail.com   ← alumno con cuota POR VENCER (recibirá aviso)")
    print("   hernestolopez2026@gmail.com ← alumno SUSPENDIDO por cuota vencida")
