from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioAlumnoModel, ProfesorModel

#USUARIOSALUMNOS = {
#    1: {'nombre':'Federico', 'rol':'Alumno'},
#    2: {'nombre':'Benjamin', 'rol':'Alumno'}
#}

#USUARIOS_PROFESOR = {
#    1: {"nombre":"Armando","apellido":"Barreras"},
#    2: {"nombre":"Felix","apellido":"Barrios"}
#}        

class UsuarioAlumno(Resource):
    def get(self, id):
        usuarioalumno = db.session.query(UsuarioAlumnoModel).get_or_404(id)
        return usuarioalumno.to_json()

    def delete(self, id):
        usuarioalumno = db.session.query(UsuarioAlumnoModel).get_or_404(id)
        db.session.delete(usuarioalumno)
        db.session.commit()
        return '', 204

    def put(self, id):
        usuarioalumno = db.session.query(UsuarioAlumnoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuarioalumno, key, value)
        db.session.add(usuarioalumno)
        db.session.commit()
        return usuarioalumno.to_json() , 201

class UsuariosAlumnos(Resource):
    def get(self):
        usuariosalumnos = db.session.query(UsuarioAlumnoModel).all()
        return jsonify([usuarioalumno.to_json() for usuarioalumno in usuariosalumnos])


    def post(self):
        usuarioalumno = UsuarioAlumnoModel.from_json(request.get_json())
        db.session.add(usuarioalumno)
        db.session.commit()
        return usuarioalumno.to_json(), 201
    

class UsuarioProfesor(Resource):
    def get(self,id):
        usuarioprofesor = db.session.query(ProfesorModel).get_or_404(id)
        return usuarioprofesor.to_json()
    

    def put(self, id):
        usuarioprofesor = db.session.query(ProfesorModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuarioprofesor, key, value)
        db.session.add(usuarioprofesor)
        db.session.commit()
        return usuarioprofesor.to_json() , 201
