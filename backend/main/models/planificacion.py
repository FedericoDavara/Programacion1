from .. import db

class Planificacion(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    tipo_planificacion = db.Column(db.String(100), nullable = False)
    horario = db.column(db.String(100),nullable = False)
    fecha = db.column(db.String(100),nullable = False)
    
    def __repr__(self):
        return '<Planificacion : %r %r %r >' & (self.tipo_planificacion, self.horario), self.fecha
    
        
    def to_json(self):
        planificacion_json = {
            'id' : self.id,
            'tipo_planificacion' : str(self.tipo_planificacion),
            'horario' : str(self.horario),
            'fecha' : str(self.fecha)         
        
        
        }
        return planificacion_json
    
    def to_json_short(self):
        planificacion_json = {
            'id' : self.id,
            'tipo_planificacion' : str(self.tipo_planificacion),
            'horario' : str(self.horario),
            'fecha' : str(self.fecha)
            
        }
        return planificacion_json
    
    @staticmethod
    def from_json(planificacion_json):
        id = planificacion_json.get('id')
        tipo_pĺanificacion = planificacion_json.get('titulo')
        horario = planificacion_json.get('especialidad')
        fecha = planificacion_json.get('fecha')
        return Planificacion(id=id,
                        tipo_pĺanificacion=tipo_pĺanificacion,
                        horario=horario,
                        fecha=fecha
                        )
        
        
        