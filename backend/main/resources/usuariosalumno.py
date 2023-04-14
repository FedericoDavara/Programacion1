from flask_restful import Resource
from flask import request

USUARIOSALUMNOS = {
    1: {'nombre':'Federico', 'rol':'Alumno'},
    2: {'nombre':'Benjamin', 'rol':'Alumno'}
}

USUARIOS_PROFESOR = {
    1: {"nombre":"Armando","apellido":"Barreras"},
    2: {"nombre":"Felix","apellido":"Barrios"}
}        

class UsuarioAlumno(Resource):
    def get(self, id):
        if int(id) in USUARIOSALUMNOS:
            return USUARIOSALUMNOS[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in USUARIOSALUMNOS:
            del USUARIOSALUMNOS[int(id)]
            return '', 204
        return '', 404

    def put(self, id):
        if int(id) in USUARIOSALUMNOS:
            usuario = USUARIOSALUMNOS[int(id)]
            data = request.get_json()
            usuario.update(data)
            return '', 201
        return '', 404


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
