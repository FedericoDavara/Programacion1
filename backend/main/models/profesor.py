from .. import db, sa
from . import UsuariosModel
class Profesor(db.Model):
    id_profesor = sa.Column(sa.Integer,sa.ForeignKey(UsuariosModel.dni), primary_key=True)
    titulo = sa.Column(sa.String(100), nullable=False)
    especialidad = sa.Column(sa.String(100), nullable=False)
    planificaciones = db.relationship('Planificacion', back_populates='profesor',cascade='all, delete-orphan')
    usuario = db.relationship('Usuarios', uselist = False, back_populates = 'Profesor', cascade = 'all, delete-orphan',single_parent=True)
    
    def __repr__(self):
        return (
            f'<ID: {self.id_profesor}, Titulo: {self.titulo},Especialidad{self.especialidad}'
        )
    
    def to_json(self):
        profesor_json = {
            'Id': int(self.id_profesor),
            'Titulo': str(self.titulo),
            'Especialidad': str(self.especialidad) 
        }
        return profesor_json
    
    def to_jsoon_complete(self):
        profesor_json = {
            "Especialidad": str(self.especialidad),
            "Titulo": str(self.titulo),
            "Usuario": self.usuario.to_json() if self.usuario != None else "",
            "Planificaciones": [planificacion.to_json() for planificacion in self.planificaciones]
        }
        return profesor_json



    @staticmethod
    def from_json(usuario_json):
        return Profesor(
            id_profesor=usuario_json.get('Id'),
            titulo=usuario_json.get('Titulo'),
            especialidad=usuario_json.get('Especialidad')

        )        
    
    