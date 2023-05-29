from flask_restful import Resource
from flask import request,jsonify 
from main.models import PlanificacionModel
from .. import db

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
        page, per_page = 1, 10
        if request.args.get("page"):
            page = int(request.args.get("page"))
        if request.args.get("per_page"):
            per_page = int(request.args.get("per_page"))
        plan = db.session.query(PlanificacionModel)

        if request.args.get("alumno_dni"):
            plan = plan.filter(PlanificacionModel.alumno_dni.like(request.args.get("alumno_dni")))

        if request.args.get("profesor_dni"):
            plan = plan.filter(PlanificacionModel.profesor_dni.like(request.args.get("profesor_dni")))

        if request.args.get("estado"):
            plan = plan.filter(PlanificacionModel.estado == request.args.get("estado"))

        if request.args.get('order_by_date') == 'asc':
            plan=plan.order_by(asc(PlanificacionModel.creation_date))
            
        if request.args.get('order_by_date') == 'desc':
            plan=plan.order_by(desc(PlanificacionModel.creation_date))

        plan = plan.paginate(page=page, per_page=per_page, error_out=True, max_per_page=20)
        return jsonify(
            {"Planificaciones": [plan.to_json() for plan in plan],
            "total": plan.total,
            "pages": plan.pages,
            "page": page})

    def post(self):
        try:
            plan = PlanificacionModel.from_json(request.get_json())
        except:
            return 'Formato no correcto', 400
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


