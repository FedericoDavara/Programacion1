from .. import db, sa
from . import ProfesorModel, AlumnoModel
from datetime import datetime 

class Planificacion(db.Model):
    id_rutinas = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    tipo_planficacion =sa.Column(sa.String(50), nullable=False)
    id_alumno = sa.Column(sa.Integer,sa.ForeignKey(AlumnoModel.id_alumno), nullable=False)
    id_profesor = sa.Column(sa.Integer,sa.ForeignKey(ProfesorModel.id_profesor) ,nullable=False)
    horario = sa.Column(sa.DateTime, nullable=False)
    profesor = db.relationship('Profesor', back_populates='planificaciones', uselist = False, single_parent = True)
    alumno = db.relationship("Alumno", back_populates="planificaciones", uselist = False, single_parent = True)
    
    
    def __repr__(self):
        return f'<N°Rutina: {self.id_rutinas,}, Rutina: {self.tipo_planficacion},Horario:{self.horario}'
    

    def to_json(self):
        rutina_json = {
            'id_rutinas': self.id_rutinas,
            'tipo_planificacion': self.tipo_planficacion,
            'id_alumno': self.id_alumno,
            'id_profesor': self.id_profesor,
            'horario': str(self.horario.strftime('%d/%m'))
        }
        return rutina_json
    
    def to_json_complete(self):
        rutina_json = {
            "id_rutinas": self.id_rutinas,
            'tipo_planificacion': self.tipo_planficacion,
            "horario": str(self.creation_date.strftime("%d/%m")),
            "Profesor": self.profesor.to_json() if self.profesor != None else "",
            "Alumno": self.alumno.to_json() if self.alumno != None else "",
            
        }
        return rutina_json




    @staticmethod
    def from_json(rutina_json):
        return Planificacion(
            id_alumno=rutina_json.get('id_alumno'),
            id_profesor=rutina_json.get('id_profesor'),
            horario =datetime.strptime(rutina_json.get('horario'), '%d/%m')
        )
    

    