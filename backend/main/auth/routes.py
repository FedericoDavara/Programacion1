from flask import request, jsonify, Blueprint
from datetime import datetime, timezone, timedelta
from .. import db
from main.models import UsuarioModel, AlumnoModel, ProfesorModel, CuotaModel
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from main.mail.functions import sendMail

DIAS_GRACIA = 3

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    usuario = (
        db.session.query(UsuarioModel)
        .filter(UsuarioModel.email == request.get_json().get("email"))
        .first_or_404()
    )

    if usuario.validate_pass(request.get_json().get("password")):
        # Check if user is suspended after password validation
        if usuario.is_suspended:
            return {
                "error": "suspended",
                "fecha": usuario.fecha_suspension.isoformat(),
                "motivo": usuario.motivo_suspension,
            }, 403

        access_token = create_access_token(identity=usuario)
        data = {
            "dni": str(usuario.dni),
            "email": usuario.email,
            "access_token": access_token,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "rol": usuario.rol,
        }

        return data, 200
    else:
        return "Incorrect password", 401


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    usuario = UsuarioModel.from_json(data)
    exists = (
        db.session.query(UsuarioModel)
        .filter(UsuarioModel.email == usuario.email)
        .scalar()
        is not None
    )
    if exists:
        return "Duplicated mail", 409
    else:
        try:
            db.session.add(usuario)
            db.session.commit()

            # Si el rol es 'user' (alumno), crear también el registro de Alumno
            if usuario.rol == "user":
                plan_elegido = data.get("plan", "Street Fighter II (The World Warrior)")
                alumno_data = {
                    "dni": usuario.dni,
                    "edad": data.get("edad"),
                    "peso": data.get("peso"),
                    "altura": data.get("altura"),
                    "sexo": data.get("sexo"),
                }
                alumno = AlumnoModel.from_json(alumno_data)
                alumno.plan = plan_elegido
                db.session.add(alumno)
                db.session.commit()

                # Crear primera cuota con vencimiento en 30 días
                monto = float(data.get("monto", 22000))
                cuota = CuotaModel(
                    alumno_dni=usuario.dni,
                    plan=plan_elegido,
                    monto_base=monto,
                    recargo_porcentaje=10.0,
                    fecha_emision=datetime.now(timezone.utc).replace(tzinfo=None),
                    fecha_vencimiento=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=30),
                )
                db.session.add(cuota)
                db.session.commit()

                sendMail(
                    [usuario.email],
                    "🪙 INSERT COIN — Tu primera cuota en GOL GYM",
                    "primera_cuota",
                    usuario=usuario,
                    cuota=cuota,
                    dias_gracia=DIAS_GRACIA,
                )

            # Si el rol es 'profesor', crear también el registro de Profesor
            if usuario.rol == "profesor":
                profesor_data = {
                    "dni": usuario.dni,
                    "especialidad": data.get("especialidad"),
                }
                profesor = ProfesorModel.from_json(profesor_data)
                db.session.add(profesor)
                db.session.commit()

            sent = sendMail([usuario.email], "¡Bienvenido a GOL GYM!", "register", usuario=usuario)
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return usuario.to_json_complete(), 201
