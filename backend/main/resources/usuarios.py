from flask_restful import Resource
from flask import request

USUARIOS = {
    1: {'nombre':'Federico', 'rol':'Alumno'},
    2: {'nombre':'Benjamin', 'rol':'Alumno'}
}

USUARIOS_PROFESOR = {
    1: {"nombre":"Armando","apellido":"Barreras"},
    2: {"nombre":"Felix","apellido":"Barrios"}
}        


class UsuarioAlumno(Resource):
    def get(self, id):
        if int(id) in USUARIOS:
            return USUARIOS[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in USUARIOS:
            del USUARIOS[int(id)]
            return '', 204
        return '', 404

    def put(self, id):
        if int(id) in USUARIOS:
            usuario = USUARIOS[int(id)]
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


class UsuarioProfesor(Resource):
    def get(self,id):
        if int(id) in USUARIOS_PROFESOR:
            return USUARIOS_PROFESOR[int(id)]
        return "", 404
    
    def put(self,id):
        if int(id) in USUARIOS_PROFESOR:
            usuario = USUARIOS_PROFESOR[int(id)]
            data = request.get_json()
            usuario.update(data)
            return "", 201
        return "", 404
    
    
    