from .. import db
from . import AlumnoModel
from datetime import datetime, timezone

DIAS_GRACIA = 3


class Cuota(db.Model):
    __tablename__ = "cuota"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumno_dni = db.Column(db.Integer, db.ForeignKey(AlumnoModel.dni), nullable=False)
    plan = db.Column(db.String(150), nullable=False)
    monto_base = db.Column(db.Float, nullable=False)
    recargo_porcentaje = db.Column(db.Float, nullable=False, default=10.0)
    fecha_emision = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    fecha_vencimiento = db.Column(db.DateTime, nullable=False)
    fecha_pago = db.Column(db.DateTime, nullable=True)
    intentos_cobro = db.Column(db.Integer, nullable=False, default=0)

    alumno = db.relationship("Alumno", back_populates="cuotas")

    @property
    def estado(self):
        if self.fecha_pago is not None:
            return "AL_DIA"
        hoy = datetime.now(timezone.utc).replace(tzinfo=None)
        venc = self.fecha_vencimiento
        dias_restantes = (venc - hoy).days
        if dias_restantes > DIAS_GRACIA:
            return "PENDIENTE"
        if 0 <= dias_restantes <= DIAS_GRACIA:
            return "POR_VENCER"
        # vencida
        if self.intentos_cobro < DIAS_GRACIA:
            return "RECHAZADO"
        return "VENCIDA"

    @property
    def monto_total(self):
        hoy = datetime.now(timezone.utc).replace(tzinfo=None)
        if self.fecha_pago is None and self.fecha_vencimiento < hoy:
            return round(self.monto_base * (1 + self.recargo_porcentaje / 100), 2)
        return self.monto_base

    def to_json(self):
        return {
            "id": self.id,
            "alumno_dni": self.alumno_dni,
            "plan": self.plan,
            "monto_base": self.monto_base,
            "monto_total": self.monto_total,
            "recargo_porcentaje": self.recargo_porcentaje,
            "fecha_emision": self.fecha_emision.isoformat() if self.fecha_emision else None,
            "fecha_vencimiento": self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            "fecha_pago": self.fecha_pago.isoformat() if self.fecha_pago else None,
            "intentos_cobro": self.intentos_cobro,
            "estado": self.estado,
        }

    def to_json_short(self):
        return {
            "id": self.id,
            "plan": self.plan,
            "monto_total": self.monto_total,
            "fecha_vencimiento": self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            "fecha_pago": self.fecha_pago.isoformat() if self.fecha_pago else None,
            "estado": self.estado,
        }

    @staticmethod
    def from_json(data):
        fecha_venc = data.get("fecha_vencimiento")
        if isinstance(fecha_venc, str):
            fecha_venc = datetime.fromisoformat(fecha_venc)
        return Cuota(
            alumno_dni=data.get("alumno_dni"),
            plan=data.get("plan"),
            monto_base=float(data.get("monto_base", 0)),
            recargo_porcentaje=float(data.get("recargo_porcentaje", 10.0)),
            fecha_emision=datetime.now(timezone.utc).replace(tzinfo=None),
            fecha_vencimiento=fecha_venc,
        )
