from flask_restful import Resource
from flask import request,jsonify 
from main.models import PlanificacionModel
from .. import db
"""PLANIFICACIONES ={
    1:{1:"Press de Banca",2:"Sentadillas",3:"Remos con barra",4:"Press militar",5:"Curl de biceps",6:"Extension de triceps"},
    2:{1:"Peso muerto",2:"Flexiones de pecho",3:"Dominadas",4:"Press de hombros con mancuernas",5:"Curl de martillo", 6:"Patada de tríceps"},
    3: {1:"Sentadillas",2:"Press de banca inclinado",3:"Remo con mancuernas", 4:"Press de hombros con barra", 5:"Curl de bíceps con mancuernas", 6:"Extensión de tríceps con mancuernas"}
}"""

"""PLANIFICACION_ALUMNO = {
    1:{"id_alumno":"1","id_plan":"1"}
}"""

class PlanificacionAlumno(Resource):
    def get(self,id):
        planificacion = {
            db.session.query(PlanificacionModel).filter(
            PlanificacionModel.id_alumno == id
            )

        }.all()
        return jsonify([rutina.to_json() for rutina in planificacion])
    
    def delete(self,id):
        rutina = db.session.query(PlanificacionModel).get_or_404(id)
        db.session.delete(rutina)
        db.session.commit()
        return '', 204
    
class Planificacion(Resource):
    def get(self):
        planificacion = db.session.query(PlanificacionModel).all()
        response = jsonify({rutina.to_json() for rutina in planificacion})
        return response
    def post(self):
        plan = PlanificacionModel.from_json(request.get_json())
        db.session.add(plan)
        db.session.commit()
        return plan.to_json(), 201    
    
class PlanificacionProfesor(Resource):
    def get(self, dni):
        planificacion = (
            db.session.query(PlanificacionModel).filter(
                PlanificacionModel.profesor_DNI == dni
            )
        ).all()
        return jsonify([plan.to_json() for plan in planificacion])

    def delete(self, dni):
        plan = db.session.query(PlanificacionModel).get_or_404(dni)
        db.session.delete(plan)
        db.session.commit()
        return '', 204

    def put(self, dni):
        plan = db.session.query(PlanificacionModel).filter(PlanificacionModel.profesor_DNI == dni).first()
        data = request.get_json().items()
        for key, value in data:
            setattr(plan, key, value)
        db.session.add(plan)
        db.session.commit()
        return plan.to_json() , 201 


