from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import UsuariosModel,AlumnoModel
import regex
from datetime import datetime
from sqlalchemy import func, desc, asc


class UsuarioAlumno(Resource):
    def get(self, id_alumno):
        alumno = db.session.query(AlumnoModel).get_or_404(id_alumno)
        return alumno.to_json_complete()

    def put(self, id_alumno):
        alumno = db.session.query(AlumnoModel).get_or_404(id_alumno)
        data = request.get_json().items()
        for key, value in data:
            setattr(alumno, key.lower(), value)
        db.session.add(alumno)
        db.session.commit()
        return alumno.to_json(), 201
    
class UsuariosAlumnos(Resource):
    def get(self):
        page=1
        per_page=10
        alumnos = db.session.query(AlumnoModel)
        if request.args.get('page'):
            page=int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page=int(request.args.get('per_page'))
        if 'by_edad' in request.args.keys():
            alumnos = alumnos.order_by(asc(AlumnoModel.edad))
        if 'by_id_alumno' in request.args.keys():
            alumnos = alumnos.order_by(desc(AlumnoModel.id_alumno))
        alumnos = alumnos.paginate(page=page, per_page=per_page, error_out=True, max_per_page=20)
        return jsonify({
            "alumnos":[alumnos.to_json() for alumnos in alumnos],
            "total": alumnos.total,
            "pages": alumnos.pages,
            "page": alumnos.page
            })

    def post(self):
        alumno = AlumnoModel.from_json(request.get_json())
        exist = db.session.query(UsuariosModel).get_or_404(alumno.id_alumno)
        try:
            db.session.add(alumno)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return alumno.to_json(), 201