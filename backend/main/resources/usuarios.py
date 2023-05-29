from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import UsuariosModel
import regex
from datetime import datetime
from sqlalchemy import func, desc, asc

class Usuario(Resource):
    def get(self, dni):
        usuario = db.session.query(UsuariosModel).get_or_404(dni)
        return usuario.to_json_complete()

    def put(self, dni):
        usuario = db.session.query(UsuariosModel).get_or_404(dni)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key.lower(), value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201        

    def delete(self, dni):
        usuario = db.session.query(UsuariosModel).get_or_404(dni)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class Usuarios(Resource):
    def get(self):
        page=1
        per_page=10
        usuarios = db.session.query(UsuariosModel)
        if request.args.get('page'):
            page=int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page=int(request.args.get('per_page'))
        if request.args.get('status'):
            usuarios = usuarios.filter(UsuariosModel.estado == request.args.get('status'))
        if 'by_lastname' in request.args.keys():
            usuarios = usuarios.order_by(asc(UsuariosModel.apellidos))
        if 'by_dni' in request.args.keys():
            usuarios = usuarios.order_by(desc(UsuariosModel.dni))
        usuarios = usuarios.paginate(page=page, per_page=per_page, error_out=True, max_per_page=20)
        return jsonify({
            "usuarios":[usuario.to_json_complete() for usuario in usuarios],
            "total": usuarios.total,
            "pages": usuarios.pages,
            "page": usuarios.page
            })

    def post(self):
        usuario = UsuariosModel.from_json(request.get_json())
        try:
            db.session.add(usuario)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return usuario.to_json(), 201

    
