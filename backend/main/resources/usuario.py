from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import (
    UsuarioModel,
    AlumnoModel,
    ProfesorModel,
    PlanificacionModel,
    ClaseModel,
)
from sqlalchemy import func, desc, or_, and_
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required
from main.mail.functions import sendMail
from datetime import datetime


def validate_json_data(data, required_fields):
    """Valida que los datos JSON contengan los campos requeridos"""
    if not data:
        raise ValueError("No se recibieron datos JSON")

    missing_fields = []
    for field in required_fields:
        if (
            field not in data
            or data[field] is None
            or (isinstance(data[field], str) and not data[field].strip())
        ):
            missing_fields.append(field)

    if missing_fields:
        raise ValueError(
            f"Los siguientes campos son requeridos: {', '.join(missing_fields)}"
        )

    return True


class Usuario(Resource):
    @jwt_required()
    def get(self, dni):
        usuario = db.session.query(UsuarioModel).get_or_404(dni)
        current_identity = get_jwt_identity()
        if current_identity:
            return usuario.to_json_complete()
        else:
            return usuario.to_json()

    @role_required(roles=["admin", "profesor"])
    def delete(self, dni):
        usuario = db.session.query(UsuarioModel).get_or_404(dni)
        current_identity = get_jwt_identity()
        # Obtener el usuario autenticado
        usuario_actual = db.session.query(UsuarioModel).get(current_identity)
        # Si es profesor, solo puede borrar alumnos
        if usuario_actual and usuario_actual.rol == "profesor":
            if usuario.rol != "user":
                return {"error": "Solo puedes eliminar usuarios con rol alumno."}, 403
        db.session.delete(usuario)
        db.session.commit()
        return "", 204

    @jwt_required()
    def put(self, dni):
        usuario = db.session.query(UsuarioModel).get_or_404(dni)
        data = request.get_json()
        current_identity = get_jwt_identity()
        usuario_actual = db.session.query(UsuarioModel).get(current_identity)

        try:
            # Check if data contains suspension fields
            has_suspension_fields = (
                "fecha_suspension" in data or "motivo_suspension" in data
            )

            if has_suspension_fields:
                # Permission check: Only admin or profesor can suspend users
                if not usuario_actual or usuario_actual.rol not in [
                    "admin",
                    "profesor",
                ]:
                    return {
                        "error": "Solo administradores y profesores pueden suspender usuarios"
                    }, 403

                # Permission check: Profesor can only suspend users (rol == "user")
                if usuario_actual.rol == "profesor" and usuario.rol != "user":
                    return {
                        "error": "Los profesores solo pueden suspender alumnos"
                    }, 403

                # Get old suspension state before modification
                was_suspended = usuario.fecha_suspension is not None

                # Handle fecha_suspension
                if "fecha_suspension" in data:
                    fecha_value = data["fecha_suspension"]
                    if fecha_value is None:
                        usuario.fecha_suspension = None
                    elif isinstance(fecha_value, str):
                        # Convert ISO format string to datetime
                        usuario.fecha_suspension = datetime.fromisoformat(fecha_value)
                    else:
                        usuario.fecha_suspension = fecha_value

                # Handle motivo_suspension
                if "motivo_suspension" in data:
                    usuario.motivo_suspension = data["motivo_suspension"]

                db.session.add(usuario)
                db.session.flush()  # Ensure the object is updated with the data from data dict

                # Determine action and send appropriate email
                is_suspended_now = usuario.fecha_suspension is not None

                if is_suspended_now:
                    # User is suspended (new or updated) - send suspension email
                    sent = sendMail(
                        [usuario.email],
                        "Suspensión de cuenta",
                        "suspension",
                        usuario=usuario,
                        motivo=usuario.motivo_suspension or "No especificado",
                        fecha=usuario.fecha_suspension.isoformat()
                        if usuario.fecha_suspension
                        else "",
                    )
                    if sent:
                        print(f"INFO: Email de suspensión enviado a {usuario.email}")
                elif was_suspended and not is_suspended_now:
                    # User is being activated - send activation email
                    sent = sendMail(
                        [usuario.email],
                        "Activación de cuenta",
                        "activacion",
                        usuario=usuario,
                    )
                    if sent:
                        print(f"INFO: Email de activación enviado a {usuario.email}")
            else:
                # Handle other field updates (non-suspension related)
                for key, value in data.items():
                    # Si la clave que se está actualizando es la contraseña, cifra la nueva contraseña
                    if key == "password":
                        usuario.plain_password = (
                            value  # Utiliza el setter para cifrar la contraseña
                        )
                    elif key == "especialidad" and usuario.profesor:
                        usuario.profesor.especialidad = value
                    elif key == "edad" and usuario.alumno:
                        usuario.alumno.edad = value
                    elif key == "peso" and usuario.alumno:
                        usuario.alumno.peso = value
                    elif key == "altura" and usuario.alumno:
                        usuario.alumno.altura = value
                    elif key == "sexo" and usuario.alumno:
                        usuario.alumno.sexo = value
                    elif hasattr(usuario, key):
                        setattr(usuario, key, value)

            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(), 200
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": "Error interno del servidor"}, 500


class Usuarios(Resource):
    @jwt_required()
    def get(self):
        role = request.args.get("rol")
        page = 1
        per_page = 10
        usuarios = db.session.query(UsuarioModel)

        if request.args.get("page"):
            page = int(request.args.get("page"))
        if request.args.get("per_page"):
            per_page = int(request.args.get("per_page"))

        ### FILTROS ###

        # Busqueda por nombre (Input busqueda)

        if request.args.get("search_term"):
            search_term = request.args.get("search_term")
            search_terms = search_term.split(" ")

            if len(search_terms) == 1:
                # Si solo hay un término en la búsqueda, busca en el nombre o en el apellido.
                usuarios = usuarios.filter(
                    or_(
                        UsuarioModel.nombre.like(f"%{search_term}%"),
                        UsuarioModel.apellido.like(f"%{search_term}%"),
                    )
                )
            else:
                # Si hay dos términos, busca en el nombre y en el apellido.
                usuarios = usuarios.filter(
                    and_(
                        UsuarioModel.nombre.like(f"%{search_terms[0]}%"),
                        UsuarioModel.apellido.like(f"%{search_terms[1]}%"),
                    )
                )

        # Busqueda por rol 'user'
        if request.args.get("user"):
            usuarios = usuarios.filter(UsuarioModel.rol == "user")

        # Busqueda por rol 'profesor'
        if request.args.get("profesor"):
            usuarios = usuarios.filter(UsuarioModel.rol == "profesor")

        if role:
            usuarios = usuarios.filter(UsuarioModel.rol == role)

        ### FIN FILTROS ####

        # Ordenar por nombre alfabéticamente
        usuarios = usuarios.order_by(UsuarioModel.nombre)

        # Obtener valor paginado
        usuarios = usuarios.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=30
        )

        return jsonify(
            {
                "usuarios": [usuario.to_json() for usuario in usuarios],
                "total": usuarios.total,
                "pages": usuarios.pages,
                "page": page,
            }
        )

    @role_required(roles=["admin"])
    def post(self):
        try:
            usuarios = UsuarioModel.from_json(request.get_json())
            print(usuarios)
            db.session.add(usuarios)
            db.session.commit()
            return usuarios.to_json(), 201
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": "Formato no correcto o error interno"}, 400


class UsuarioAlumno(Resource):
    @jwt_required()
    def get(self, dni):
        usuario_a = db.session.query(AlumnoModel).get(int(dni))
        if usuario_a is None:
            return {"error": "Alumno no encontrado"}, 404
        return usuario_a.to_json_complete()

    @role_required(roles=["admin"])
    def put(self, dni):
        usuario_a = db.session.query(AlumnoModel).get(int(dni))
        if usuario_a is None:
            return {"error": "Alumno no encontrado"}, 404
        data = request.get_json().items()
        try:
            for key, value in data:
                setattr(usuario_a, key, value)
            db.session.add(usuario_a)
            db.session.commit()
            return usuario_a.to_json_complete(), 201
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": "Error interno del servidor"}, 500

    @role_required(roles=["admin", "profesor"])
    def delete(self, dni):
        usuario_a = db.session.query(AlumnoModel).get_or_404(dni)
        db.session.delete(usuario_a)
        db.session.commit()
        return "", 204


class UsuariosAlumnos(Resource):
    @role_required(roles=["admin", "profesor"])
    def get(self):
        page = 1
        per_page = 10

        usuarios_a = db.session.query(AlumnoModel)

        if request.args.get("page"):
            page = int(request.args.get("page"))
        if request.args.get("per_page"):
            per_page = int(request.args.get("per_page"))

        ### FILTROS ###
        if request.args.get("nrPlanificaciones"):
            usuarios_a = (
                usuarios_a.outerjoin(AlumnoModel.planificaciones)
                .group_by(AlumnoModel.id)
                .having(
                    func.count(PlanificacionModel.id)
                    >= int(request.args.get("nrPlanificaciones"))
                )
            )

        # Busqueda por name
        if request.args.get("nombre"):
            usuarios_a = usuarios_a.filter(
                AlumnoModel.nombre.like("%" + request.args.get("nombre") + "%")
            )
        # Ordeno por name
        if request.args.get("sortby_nombre"):
            usuarios_a = usuarios_a.order_by(desc(AlumnoModel.nombre))

        # Busqueda por apellido
        if request.args.get("apellido"):
            usuarios_a = usuarios_a.filter(
                AlumnoModel.apellido.like("%" + request.args.get("apellido") + "%")
            )
        # Ordeno por apellido
        if request.args.get("sortby_apellido"):
            usuarios_a = usuarios_a.order_by(desc(AlumnoModel.apellido))

        # Ordeno por id de Planificacion
        if request.args.get("sortby_nrPlanificaciones"):
            usuarios_a = (
                usuarios_a.outerjoin(AlumnoModel.planificaciones)
                .group_by(AlumnoModel.id)
                .order_by(func.count(PlanificacionModel.id).desc())
            )

        ### FIN FILTROS ####

        # Obtener valor paginado
        usuarios_a = usuarios_a.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=30
        )

        return jsonify(
            {
                "usuarios": [usuario_a.to_json() for usuario_a in usuarios_a],
                "total": usuarios_a.total,
                "pages": usuarios_a.pages,
                "page": page,
            }
        )

    @role_required(roles=["admin"])
    def post(self):
        try:
            usuarios_a = AlumnoModel.from_json(request.get_json())
            print(usuarios_a)
            db.session.add(usuarios_a)
            db.session.commit()
            return usuarios_a.to_json(), 201
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": "Formato no correcto o error interno"}, 400


class UsuariosProfesores(Resource):
    @jwt_required(optional=True)
    def get(self):
        usuarios_p = db.session.query(ProfesorModel).all()
        resultados = []

        for usuario_p in usuarios_p:
            nombre = usuario_p.usuario.nombre if usuario_p.usuario else None
            apellido = usuario_p.usuario.apellido if usuario_p.usuario else None
            resultado = {
                "dni": usuario_p.dni,
                "especialidad": usuario_p.especialidad,
                "nombre": nombre,
                "apellido": apellido,
            }
            resultados.append(resultado)
        return jsonify(resultados)

    @role_required(roles=["admin"])
    def post(self):
        try:
            usuarios_p = ProfesorModel.from_json(request.get_json())
            print(usuarios_p)
            db.session.add(usuarios_p)
            db.session.commit()
            return usuarios_p.to_json(), 201
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": "Formato no correcto o error interno"}, 400


class UsuarioProfesor(Resource):
    @jwt_required(optional=True)
    def get(self, dni):
        usuario_p = db.session.query(ProfesorModel).get_or_404(dni)
        return usuario_p.to_json()

    @role_required(roles=["admin"])
    def put(self, dni):
        usuario_p = db.session.query(ProfesorModel).get_or_404(dni)
        data = request.get_json().items()
        try:
            for key, value in data:
                setattr(usuario_p, key, value)
            db.session.add(usuario_p)
            db.session.commit()
            return usuario_p.to_json(), 200
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": "Error interno del servidor"}, 500
