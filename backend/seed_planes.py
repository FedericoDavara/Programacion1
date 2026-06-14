"""
Script para cargar los 5 planes Street Fighter en la tabla Precios.
Uso: python3 seed_planes.py
"""
from app import app
from main import db
from main.models import PrecioModel

PLANES = [
    {
        "nombre": "Street Fighter II (The World Warrior)",
        "precio": "$22.000 ARS",
        "descripcion": "El clásico que lo empezó todo. Acceso a musculación 2 o 3 veces por semana. El mundo no se conquista de un día. 🥋",
    },
    {
        "nombre": "Street Fighter II Turbo (Hyper Fighting)",
        "precio": "$28.000 ARS",
        "descripcion": "Pusiste el turbo. Musculación con pase libre + acceso a clases grupales seleccionadas. Más velocidad, más opciones. ⚡",
    },
    {
        "nombre": "Super Street Fighter II Turbo (The Ultimate Championship)",
        "precio": "$35.000 ARS",
        "descripcion": "El nombre más largo para el plan más completo. Pase libre total + todas las clases + casillero asignado. Vos ya no venís al gym, vos llegás. 🔥",
    },
    {
        "nombre": "Ultra Street Fighter IV (Arcade Edition)",
        "precio": "$42.000 ARS",
        "descripcion": "Para los que van en serio. Pase libre total + rutina personalizada con profe + beneficios en suplementos. Cuatro versiones y recién en esta pusieron todo. 👑",
    },
    {
        "nombre": "Super Street Fighter II: The New Challengers",
        "precio": "$24.000 ARS por persona",
        "descripcion": "Porque los mejores combates son en equipo. Plan grupal/familiar: amigos, parejas o grupos. Traé a tu crew y activen el modo cooperativo. 👥",
    },
]

with app.app_context():
    eliminados = db.session.query(PrecioModel).delete()
    print(f"Precios anteriores eliminados: {eliminados}")
    db.session.commit()

    for p in PLANES:
        precio = PrecioModel(
            nombre=p["nombre"],
            precio=p["precio"],
            descripcion=p["descripcion"],
        )
        db.session.add(precio)

    db.session.commit()
    print(f"✅ {len(PLANES)} planes cargados exitosamente:")
    for plan in db.session.query(PrecioModel).all():
        print(f"  [{plan.id}] {plan.nombre} — {plan.precio}")
