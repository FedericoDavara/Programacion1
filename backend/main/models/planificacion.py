from .. import db
import json
from datetime import datetime

class Planificacion(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    tipo_planificacion = db.Column(db.String(100), nullable = False)
    horario = db.column(db.String(100),nullable = False)
    fecha = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return '<Planificacion : %r >' & (self.tipo_planificacion)
    
        
    def to_json(self):
        planificacion_json = {
            'id' : self.id,
            'tipo_planificacion' : str(self.tipo_planificacion),
            'horario' : str(self.horario),
            'fecha' : str(self.fecha.strftime("%d-%m-%Y")) 
        }
        return planificacion_json
    
    def to_json_short(self):
        planificacion_json = {
            'id' : self.id,
            'tipo_planificacion' : str(self.tipo_planificacion),
            'horario' : str(self.horario),
            'fecha' :  str(self.fecha.strftime("%d-%m-%Y"))
            
        }
        return planificacion_json
    
    @staticmethod
    def from_json(planificacion_json):
        id = planificacion_json.get('id')
        tipo_pĺanificacion = planificacion_json.get('titulo')
        horario = planificacion_json.get('especialidad')
        fecha = datetime.strptime(planificacion_json.get('fecha'), '%d-%m-%Y')
        return Planificacion(id=id,
                        tipo_pĺanificacion=tipo_pĺanificacion,
                        horario=horario,
                        fecha=fecha
                        )
        
        