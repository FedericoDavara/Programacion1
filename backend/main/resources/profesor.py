from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProfesorModel

class ProfesorClases(Resource):
     def get(self):
        usuarioprofesor = db.session.query(ProfesorModel).get_or_404(id)
        return usuarioprofesor.to_json()
    