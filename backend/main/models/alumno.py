from .. import db  # Importa el módulo "db" desde el paquete superior

from . import UsuarioModel  # Importa la clase "UsuarioModel" desde el paquete actual

class Alumno(db.Model):
    dni = db.Column(db.Integer, db.ForeignKey(UsuarioModel.dni), primary_key=True)  # Columna de la base de datos para el DNI del alumno
    edad = db.Column(db.Integer, nullable=False)  # Columna de la base de datos para la edad del alumno
    peso = db.Column(db.Integer, nullable=False)  # Columna de la base de datos para el peso del alumno
    altura = db.Column(db.Integer, nullable=False)  # Columna de la base de datos para la altura del alumno
    sexo = db.Column(db.String(100), nullable=False)  # Columna de la base de datos para el sexo del alumno

    usuario = db.relationship("Usuario", uselist=False, back_populates="alumno",  # Relación uno a uno entre Alumno y Usuario
                              cascade="all, delete-orphan", single_parent=True)

    planificaciones = db.relationship("Planificacion", back_populates="alumno",  # Relación uno a muchos entre Alumno y Planificacion
                                      cascade="all, delete-orphan")

    def __repr__(self):
        return '<Usuario: %r %r %r %r>' % (self.edad, self.peso, self.altura, self.sexo)
        # Representación de cadena para la clase Alumno

    def to_json(self):
        alumno_json = {
            'dni': str(self.dni),
            'edad': str(self.edad),
            'peso': str(self.peso),
            'altura': str(self.altura),
            'sexo': str(self.sexo)
        }
        return alumno_json
        # Convierte el objeto Alumno en un diccionario JSON

    def to_json_complete(self):
        planificaciones = [planificacion.to_json() for planificacion in self.planificaciones]
        alumno_json = {
            'dni': str(self.dni),
            'edad': str(self.edad),
            'peso': str(self.peso),
            'altura': str(self.altura),
            'sexo': str(self.sexo),
            'planificaciones': planificaciones
        }
        return alumno_json
        # Convierte el objeto Alumno en un diccionario JSON completo, incluyendo las planificaciones asociadas

    def to_json_short(self):
        alumno_json = {
            'dni': str(self.dni),
            'edad': str(self.edad),
            'peso': str(self.peso),
            'altura': str(self.altura),
            'sexo': str(self.sexo)
        }
        return alumno_json
        # Convierte el objeto Alumno en un diccionario JSON corto, sin incluir las planificaciones

    @staticmethod
    def from_json(alumno_json):
        dni = alumno_json.get('dni')
        edad = alumno_json.get('edad')
        peso = alumno_json.get('peso')
        altura = alumno_json.get('altura')
        sexo = alumno_json.get('sexo')
        return Alumno(dni=dni, edad=edad, peso=peso, altura=altura, sexo=sexo)
        # Crea un objeto Alumno a partir de un diccionario JSON
