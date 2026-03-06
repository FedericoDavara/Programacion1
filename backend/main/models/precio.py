from .. import db
import re
from sqlalchemy.orm import validates


class Precio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)  # e.g. "1 Mes", "3 Meses"
    precio = db.Column(db.String(50), nullable=False)  # e.g. "$12.000"
    descripcion = db.Column(
        db.String(250), nullable=True
    )  # e.g. "1 mes de suscripción estándar."

    @validates("nombre")
    def validate_nombre(self, key, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("Nombre del precio es requerido")
        if len(nombre.strip()) < 2:
            raise ValueError("Nombre del precio debe tener al menos 2 caracteres")
        if len(nombre.strip()) > 50:
            raise ValueError("Nombre del precio no puede exceder 50 caracteres")
        return nombre.strip()

    @validates("precio")
    def validate_precio(self, key, precio):
        if not precio or not precio.strip():
            raise ValueError("Precio es requerido")
        return precio.strip()

    def __repr__(self):
        return "<Precio: %r %r>" % (self.nombre, self.precio)

    def to_json(self):
        return {
            "id": self.id,
            "nombre": str(self.nombre),
            "precio": str(self.precio),
            "descripcion": str(self.descripcion) if self.descripcion else None,
        }

    def to_json_short(self):
        return self.to_json()

    @staticmethod
    def from_json(precio_json):
        id = precio_json.get("id")
        nombre = precio_json.get("nombre")
        precio = precio_json.get("precio")
        descripcion = precio_json.get("descripcion")
        return Precio(id=id, nombre=nombre, precio=precio, descripcion=descripcion)
