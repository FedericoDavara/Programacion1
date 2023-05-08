from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioAlumnoModel

#USUARIOSALUMNOS = {
#    1: {'nombre':'Federico', 'rol':'Alumno'},
#    2: {'nombre':'Benjamin', 'rol':'Alumno'}
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
        usuario_id = request.args.get('usuario_id')
        
        alumnos = db.session.query(UsuarioAlumnoModel)

        
        if usuario_id:
            alumnos = alumnos.filter(UsuarioAlumnoModel.usuario_id == usuario_id)

        alumnos = alumnos.all()

        return jsonify({ 'alumnos': [usuarioalumno.to_json() for usuarioalumno in alumnos] })

    def post(self):
        usuarioalumno = UsuarioAlumnoModel.from_json(request.get_json())
        print(usuarioalumno)
        try:
            db.session.add(usuarioalumno)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return usuarioalumno.to_json(), 201