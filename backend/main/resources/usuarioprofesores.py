from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import UsuariosModel,ProfesorModel,AlumnoModel
import regex
from datetime import datetime




class UsuarioProfesor(Resource):
    def get(self, dni):
        profesor = db.session.query(ProfesorModel).get_or_404(dni)
        return profesor.to_json_complete()

    def put(self, dni):
        profesor = db.session.query(ProfesorModel).get_or_404(dni)
        data = request.get_json().items()
        for key, value in data:
            if regex.match(r"\d{2}/\d{2}/\d{4}", str(value)) != None:
                setattr(profesor, key.lower(), datetime.strptime(value, "%d/%M/%Y"))
            else: setattr(profesor, key.lower(), value)
        db.session.add(profesor)
        db.session.commit()
        return profesor.to_json() , 201

class UsuarioProfesores(Resource):
    def get(self):
        profesores = db.session.query(ProfesorModel).all()
        return jsonify([profesor.to_json() for profesor in profesores])

    def post(self):
        try:
            profesor = ProfesorModel.from_json(request.get_json())
        except:
            return 'Formato no correcto', 400
        exist = db.session.query(UsuariosModel).get_or_404(profesor.dni)
        db.session.add(profesor)
        db.session.commit()
        return profesor.to_json(), 201
    