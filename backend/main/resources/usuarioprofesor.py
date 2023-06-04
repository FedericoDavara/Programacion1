from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import UsuariosModel,ProfesorModel
import regex
from datetime import datetime




class UsuarioProfesor(Resource):
    def get(self, id_profesor):
        profesor = db.session.query(ProfesorModel).get_or_404(id_profesor)
        return profesor.to_json_complete()

    def put(self, id_profesor):
        profesor = db.session.query(ProfesorModel).get_or_404(id_profesor)
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
        page=1
        per_page=10
        profesor = db.session.query(ProfesorModel)
        if request.args.get('page'):
            page=int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page=int(request.args.get('per_page'))
        if 'by_especialidad' in request.args.keys():
            profesor = profesor.order_by(asc(ProfesorModel.especialidad))
        if 'by_id_profesor' in request.args.keys():
            profesor = profesor.order_by(desc(ProfesorModel.id_profesor))
        profesor = profesor.paginate(page=page, per_page=per_page, error_out=True, max_per_page=20)
        return jsonify({
            "profesores":[profesor.to_json() for profesor in profesor],
            "total": profesor.total,
            "pages": profesor.pages,
            "page": profesor.page
            })
    
    def post(self):
        try:
            profesor = ProfesorModel.from_json(request.get_json())
        except:
            return 'Formato no correcto', 400
        exist = db.session.query(UsuariosModel).get_or_404(profesor.id_profesor)
        db.session.add(profesor)
        db.session.commit()
        return profesor.to_json(), 201
    
    