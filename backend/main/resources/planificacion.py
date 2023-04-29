from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PlanificacionModel

class PlanificacionAlumno(Resource):
    def get(self,id):
        planificacionalumno = db.session.query(PlanificacionModel).get_or_404(id)
        return planificacionalumno.to_json()
    
class PlanificacionesProfesores(Resource):
    def get(self):
        planificacionesprofesores = db.session.query(PlanificacionModel).get_or_404(id)
        return planificacionesprofesores.to_json()

    def post(self):
        planificacionesprofesores = PlanificacionModel.from_json(request.get_json())
        db.session.add(planificacionesprofesores)
        db.session.commit()
        return planificacionesprofesores.to_json(), 201
    
class PlanificacionProfesor(Resource):
    def get(self,id):
        planificacionprofesor = db.session.query(PlanificacionModel).get_or_404(id)
        return planificacionprofesor.to_json()
    
    def put(self,id):
        planificacionprofesor = db.session.query(PlanificacionModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(planificacionprofesor, key, value)
        db.session.add(planificacionprofesor)
        db.session.commit()
        return planificacionprofesor.to_json() , 201

    
    def delete(self,id):
        planificacionprofesor = db.session.query(PlanificacionModel).get_or_404(id)
        db.session.delete(planificacionprofesor)
        db.session.commit()
        return '', 204
    