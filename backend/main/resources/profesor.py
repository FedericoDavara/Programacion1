from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProfesorModel



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

   def delete(self, id):
      usuarioprofesor = db.session.query(ProfesorModel).get_or_404(id)
      db.session.delete(usuarioprofesor)
      db.session.commit()
      return '', 204

class UsuariosProfesores(Resource):
   def get(self):
      usuario_id = request.args.get('usuario_id')
        
      profesores = db.session.query(ProfesorModel)

      if usuario_id:
         profesores = profesores.filter(ProfesorModel.usuario_id == usuario_id)

      profesores = profesores.all()

      return jsonify({ 'profesores': [usuarioprofesor.to_json() for usuarioprofesor in profesores] })

   def post(self):
      usuarioprofesor = ProfesorModel.from_json(request.get_json())
      print(usuarioprofesor)
      try:
         db.session.add(usuarioprofesor)
         db.session.commit()
      except:
         return 'Formato no correcto', 400
      return usuarioprofesor.to_json(), 201