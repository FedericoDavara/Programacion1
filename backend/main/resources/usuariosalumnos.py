from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import UsuariosModel,ProfesorModel,AlumnoModel
import regex
from datetime import datetime



class UsuarioAlumno(Resource):
    def get(self, dni):
        alumno = db.session.query(AlumnoModel).get_or_404(dni)
        return alumno.to_json_complete()

    def put(self, dni):
        alumno = db.session.query(AlumnoModel).get_or_404(dni)
        data = request.get_json().items()
        for key, value in data:
            setattr(alumno, key.lower(), value)
        db.session.add(alumno)
        db.session.commit()
        return alumno.to_json(), 201
    
class UsuariosAlumnos(Resource):
    def get(self):
        alumnos = db.session.query(AlumnoModel).all()
        return jsonify([alumno.to_json() for alumno in alumnos])

    def post(self):
        alumno = AlumnoModel.from_json(request.get_json())
        exist = db.session.query(UsuariosModel).get_or_404(alumno.dni)
        try:
            db.session.add(alumno)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return alumno.to_json(), 201