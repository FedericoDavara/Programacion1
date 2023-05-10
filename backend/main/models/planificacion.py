from .. import db
from datetime import datetime 

class Planificacion(db.Model):
    id_rutinas = db.Column(db.Integer, primary_key=True)
    tipo_planficacion = db.Column(db.Integer, nullable=False)
    id_alumno = db.Column(db.Integer, nullable=False)
    id_profesor = db.Column(db.Integer, nullable=False)
    horario = db.Column(db.String(10), nullable=False)


    def __repr__(self):
        return f'<N°Rutina: {self.id_rutinas,}, Rutina: {self.tipo_planficacion},Horario:{self.horario}'
    

    def to_json(self):
        rutina_json = {
            'id_rutinas': self.id_rutinas,
            'tipo_planificacion': self.tipo_planficacion,
            'id_alumno': self.id_alumno,
            'id_profesor': self.id_profesor,
            'horario': self.horario
        }
        return rutina_json
    
    @staticmethod
    def from_json(rutina_json):
        id_rutinas = rutina_json.get('id_rutinas')
        tipo_planificacion = rutina_json.get('tipo_planificacion')
        horario = rutina_json.get('horario')
        return Planificacion(
            id_alumno=rutina_json.get('id_alumno'),
            id_profesor=rutina_json.get('id_profesor')
        )
    

    