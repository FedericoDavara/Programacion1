from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import UsuariosModel,ProfesorModel,AlumnoModel


USUARIOSALUMNOS = {
    1: {'nombre':'Federico', 'rol':'Alumno'},
    2: {'nombre':'Benjamin', 'rol':'Alumno'}
}

USUARIOS_PROFESOR = {
    1: {"nombre":"Armando","apellido":"Barreras"},
    2: {"nombre":"Felix","apellido":"Barrios"}
}        



USUARIOS = {
    1: {'nombre':'Federico', 'rol':'Alumno'},
    2: {'nombre':'Benjamin', 'rol':'Alumno'},
    3: {'nombre':'Adriano', 'rol':'Alumno'}
}

class UsuarioAlumno(Resource):
    def get(self, id):
        usuario = db.session.query(UsuariosModel).get_or_404(id)
        return usuario.to_json()

    def delete(self, id):
        usuario = db.session.query(UsuariosModel).get_or_404(id)
        db.session(usuario)
        db.session.commit()
        return '', 204
    
    def put(self, dni):
        usuario = db.session.query(UsuariosModel).get_or_404(dni)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key.lower(), value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201

class UsuariosAlumnos(Resource):
    def get(self):
        return USUARIOSALUMNOS

    def post(self):
        usuario = request.get_json()
        id = int(max(USUARIOSALUMNOS.keys()))+1
        USUARIOSALUMNOS[id] = usuario
        return USUARIOSALUMNOS[id], 201
    

class UsuarioProfesor(Resource):
    def get(self,id):
        if int(id) in USUARIOS_PROFESOR:
            return USUARIOS_PROFESOR[int(id)]
        return "", 404
    

    def put(self, id):
        if int(id) in USUARIOSALUMNOS:
            usuario = USUARIOSALUMNOS[int(id)]
            data = request.get_json()
            usuario.update(data)
            return '', 201
        return '', 404

class Usuario(Resource):
    def get(self, dni):
        if int(dni) in USUARIOS:
            return USUARIOS[int(dni)]
        return '', 404

    def delete(self, dni):
        if int(dni) in USUARIOS:
            del USUARIOS[int(dni)]
            return '', 204
        return '', 404

    def put(self, dni):
        if int(dni) in USUARIOS:
            usuario = USUARIOS[int(dni)]
            data = request.get_json()
            usuario.update(data)
            return '', 201
        return '', 404


class Usuarios(Resource):
    def get(self):
        return USUARIOS

    def post(self):
        usuario = request.get_json()
        id = int(max(USUARIOS.keys()))+1
        USUARIOS[id] = usuario
        return USUARIOS[id], 201


    
    
    
