from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime, timezone, timedelta
from .. import db
from main.models import CuotaModel, AlumnoModel, UsuarioModel
from flask_jwt_extended import jwt_required
from main.auth.decorators import role_required
from main.mail.functions import sendMail

DIAS_GRACIA = 3


def _suspender_alumno(alumno, motivo="Cuota impaga"):
    alumno.estado_membresia = "SUSPENDIDO"
    usuario = alumno.usuario
    usuario.fecha_suspension = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=365)
    usuario.motivo_suspension = motivo
    db.session.commit()
    sendMail(
        [usuario.email],
        "🔴 PLAYER BLOCKED — Tu cuenta fue suspendida",
        "suspension",
        usuario=usuario,
    )


class Cuotas(Resource):
    @role_required(roles=["admin", "profesor"])
    def get(self):
        estado_filtro = request.args.get("estado")
        dni_filtro = request.args.get("alumno_dni")

        query = db.session.query(CuotaModel)
        if dni_filtro:
            query = query.filter(CuotaModel.alumno_dni == dni_filtro)

        cuotas = query.order_by(CuotaModel.fecha_vencimiento.desc()).all()

        if estado_filtro:
            cuotas = [c for c in cuotas if c.estado == estado_filtro.upper()]

        resultado = []
        for c in cuotas:
            alumno = db.session.get(AlumnoModel, c.alumno_dni)
            usuario = alumno.usuario if alumno else None
            item = c.to_json()
            if usuario:
                item["nombre"] = usuario.nombre
                item["apellido"] = usuario.apellido
                item["email"] = usuario.email
            resultado.append(item)

        resumen = {
            "total": len(resultado),
            "al_dia": sum(1 for c in cuotas if c.estado == "AL_DIA"),
            "por_vencer": sum(1 for c in cuotas if c.estado == "POR_VENCER"),
            "rechazado": sum(1 for c in cuotas if c.estado == "RECHAZADO"),
            "vencidas": sum(1 for c in cuotas if c.estado == "VENCIDA"),
            "pendientes": sum(1 for c in cuotas if c.estado == "PENDIENTE"),
        }

        return {"cuotas": resultado, "resumen": resumen}, 200

    @role_required(roles=["admin"])
    def post(self):
        try:
            data = request.get_json()
            cuota = CuotaModel.from_json(data)
            alumno = db.session.get(AlumnoModel, cuota.alumno_dni)
            if not alumno:
                return {"error": "Alumno no encontrado"}, 404

            if data.get("plan"):
                alumno.plan = data.get("plan")

            db.session.add(cuota)
            db.session.commit()

            usuario = alumno.usuario
            sendMail(
                [usuario.email],
                "🪙 INSERT COIN — Tu primera cuota en GOL GYM",
                "primera_cuota",
                usuario=usuario,
                cuota=cuota,
                dias_gracia=DIAS_GRACIA,
            )

            return cuota.to_json(), 201
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500


class Cuota(Resource):
    @jwt_required()
    def get(self, id):
        cuota = db.session.get(CuotaModel, id)
        if not cuota:
            return {"error": "Cuota no encontrada"}, 404
        return cuota.to_json(), 200

    @role_required(roles=["admin"])
    def delete(self, id):
        cuota = db.session.get(CuotaModel, id)
        if not cuota:
            return {"error": "Cuota no encontrada"}, 404
        db.session.delete(cuota)
        db.session.commit()
        return "", 204


class CuotaPagar(Resource):
    @role_required(roles=["admin"])
    def put(self, id):
        cuota = db.session.get(CuotaModel, id)
        if not cuota:
            return {"error": "Cuota no encontrada"}, 404
        if cuota.fecha_pago is not None:
            return {"error": "Esta cuota ya fue pagada"}, 400

        cuota.fecha_pago = datetime.now(timezone.utc).replace(tzinfo=None)

        alumno = db.session.get(AlumnoModel, cuota.alumno_dni)
        alumno.estado_membresia = "ACTIVO"

        # Si estaba suspendido por cuota impaga, reactivar
        usuario = alumno.usuario
        if usuario.is_suspended and "cuota" in (usuario.motivo_suspension or "").lower():
            usuario.fecha_suspension = None
            usuario.motivo_suspension = None

        # Próximo vencimiento: 30 días desde hoy
        proximo = (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=30)).strftime("%d/%m/%Y")

        db.session.commit()

        sendMail(
            [usuario.email],
            "✅ PLAYER 1 READY — Membresía activa en GOL GYM",
            "cuota_pagada",
            usuario=usuario,
            cuota=cuota,
            proximo_vencimiento=proximo,
        )

        return {"cuota": cuota.to_json(), "mail_sent": True}, 200


class CuotasAlumno(Resource):
    @jwt_required()
    def get(self, dni):
        cuotas = (
            db.session.query(CuotaModel)
            .filter(CuotaModel.alumno_dni == dni)
            .order_by(CuotaModel.fecha_vencimiento.desc())
            .all()
        )
        return {"cuotas": [c.to_json() for c in cuotas]}, 200


class ProcesarVencimientos(Resource):
    """
    Endpoint interno para procesar vencimientos.
    Marca cuotas como RECHAZADO y suspende alumnos que superaron los días de gracia.
    En producción esto debería ser un cron job o tarea programada.
    """
    @role_required(roles=["admin"])
    def post(self):
        hoy = datetime.now(timezone.utc).replace(tzinfo=None)
        cuotas_vencidas = db.session.query(CuotaModel).filter(
            CuotaModel.fecha_pago.is_(None),
            CuotaModel.fecha_vencimiento < hoy,
        ).all()

        procesadas = []
        suspendidos = []

        for cuota in cuotas_vencidas:
            alumno = db.session.get(AlumnoModel, cuota.alumno_dni)
            usuario = alumno.usuario if alumno else None
            if not usuario:
                continue

            cuota.intentos_cobro += 1
            dias_mora = (hoy - cuota.fecha_vencimiento).days
            intentos_restantes = DIAS_GRACIA - cuota.intentos_cobro

            if cuota.intentos_cobro >= DIAS_GRACIA:
                # Suspender
                _suspender_alumno(alumno, motivo="Cuota impaga — sin pago luego de 3 intentos")
                suspendidos.append(cuota.alumno_dni)
            else:
                # Notificar rechazo
                alumno.estado_membresia = "MOROSO"
                sendMail(
                    [usuario.email],
                    f"💀 GAME OVER (por ahora) — Pago no registrado, quedan {intentos_restantes} día(s)",
                    "cuota_rechazada",
                    usuario=usuario,
                    cuota=cuota,
                    intentos_restantes=intentos_restantes,
                )
                procesadas.append(cuota.alumno_dni)

        db.session.commit()

        return {
            "procesadas": len(procesadas),
            "suspendidos": len(suspendidos),
            "dni_procesados": procesadas,
            "dni_suspendidos": suspendidos,
        }, 200
