from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel, ProfesorModel, UsuarioAlumnoModel, profesor_clases
#USUARIOS = {
#    1: {'nombre':'Federico', 'rol':'Alumno'},
#    2: {'nombre':'Benjamin', 'rol':'Alumno'},
#    3: {'nombre':'Adriano', 'rol':'Alumno'}
#}

class Usuario(Resource):

    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_json_complete()

    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201


class Usuarios(Resource):
    def get(self):
        usuarios = db.session.query(UsuarioModel).all()
        return jsonify([usuario.to_json() for usuario in usuarios])

    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201
