from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import PlanificacionModel
from sqlalchemy import func, desc

class Planificacion(Resource):
    def get(self,id):
        planificacion=db.session.query(PlanificacionModel).get_or_404(id)
        return planificacion.to_json()
    
    def delete(self,id):
        planificacion=db.session.query(PlanificacionModel).get_or_404(id)
        db.session.delete(planificacion)
        db.session.commit()
        return "", 204
        
    def put(self,id):
        planificacion=db.session.query(PlanificacionModel).get_or_404(id)
        data=request.get_json().items()
        for key, value in data:
            setattr(planificacion, key, value)
        db.session.add(planificacion)
        db.session.commit()
        return planificacion.to_json(), 201

class Planificaciones(Resource):
    def get(self):
        page = 1
        per_page = 10
        
        planificaciones = db.session.query(PlanificacionModel)
        
        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))
        
        
        if request.args.get('profesor'):
            planificaciones=planificaciones.filter(PlanificacionModel.profesor_dni.like("%"+request.args.get('profesor_dni')+"%"))
        
        if request.args.get('sortby_profesor'):
            planificaciones=planificaciones.order_by(desc(PlanificacionModel.profesor_dni))

        
        if request.args.get('alumno'):
            planificaciones=planificaciones.filter(PlanificacionModel.alumno_dni.like("%"+request.args.get('alumno_dni')+"%"))
        
        if request.args.get('sortby_alumno'):
            planificaciones=planificaciones.order_by(desc(PlanificacionModel.alumno_dni))

        
        if request.args.get('fecha'):
            planificaciones=planificaciones.filter(PlanificacionModel.fecha.like("%"+request.args.get('fecha')+"%"))    
        
        if request.args.get('sortby_fecha'):
            planificaciones=planificaciones.order_by(desc(PlanificacionModel.fecha))
        
        
        planificaciones = planificaciones.paginate(page=page, per_page=per_page, error_out=True, max_per_page=30)

        return jsonify({'planificaciones': [planificacion.to_json() for planificacion in planificaciones],
                  'total': planificaciones.total,
                  'pages': planificaciones.pages,
                  'page': page
                })

    def post(self):
        planificaciones=PlanificacionModel.from_json(request.get_json())
        print(planificaciones)
        try:
            db.session.add(planificaciones)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return planificaciones.to_json(), 201

class PlanificacionAlumno(Resource):
    def get(self,dni):
        planificacion_a=db.session.query(PlanificacionModel).get_or_404(dni)
        return planificacion_a.to_json_complete()
    
class PlanificacionProfesor(Resource):
    def get(self,dni):
        planificacion_p=db.session.query(PlanificacionModel).get_or_404(dni)
        return planificacion_p.to_json()
    
    def put(self,dni):
        planificacion_p=db.session.query(PlanificacionModel).get_or_404(dni)
        data=request.get_json().items()
        for key, value in data:
            setattr(planificacion_p, key, value)
        db.session.add(planificacion_p)
        db.session.commit()
        return planificacion_p.to_json(), 201
    
    def delete(self,dni):
        planificacion_p=db.session.query(PlanificacionModel).get_or_404(dni)
        db.session.delete(planificacion_p)
        db.session.commit()
        return "", 204
    
class PlanificacionesProfesores(Resource):
    def get(self):
        dni_profesor = request.args.get("dni_profesor")
        planificaciones = db.session.query(PlanificacionModel)
        if dni_profesor:
            planificaciones = planificaciones.filter(PlanificacionModel.dni_profesor == dni_profesor)
        planificaciones = planificaciones.all()
        return jsonify({"planificaciones": [planificacion.to_json() for planificacion in planificaciones]})