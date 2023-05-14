from .. import db, sa
from . import UsuariosModel

class Alumno(db.Model):
    id_alumno = sa.Column(sa.Integer, sa.ForeignKey(UsuariosModel.dni),primary_key=True)
    edad = sa.Column(sa.Integer, nullable=False)
    peso = sa.Column(sa.Integer, nullable=False)
    altura = sa.Column(sa.Integer, nullable=False)
    usuario = db.relationship('Usuarios', uselist = False, back_populates = 'alumno',
                              cascade = 'all, delete-orphan', single_parent= True)


    def __repr__(self):
        return f'<ID: {self.id_alumno}, Edad: {self.edad}, Peso: {self.peso}, Altura: {self.altura}> '
    
    def to_json(self):
        alumno_json = {
            'ID': self.id_alumno,
            'EDAD': self.edad,
            'PESO': self.peso,
            'ALTURA': self.altura
            }
        return alumno_json
    
    def to_json_complete(self):
        alumno_json = {
            "Edad": self.edad,
            "Sexo": self.sexo,
            "Usuario": self.usuario.to_json() if self.usuario != None else "",
            "Clases": [clase.to_json() for clase in self.clases],
            "Planificaciones" : [planificacion.to_json() for planificacion in self.planificaciones]
        }
        return alumno_json


    @staticmethod
    def from_json(alumno_json):
        return Alumno(id_alumno= alumno_json.get('ID'),
                      edad= alumno_json.get('EDAD'),
                      peso= alumno_json.get('EDAD'),
                      altura= alumno_json.get('ALTURA')
                      )    