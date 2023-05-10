from .. import db

class Alumno(db.Model):
    id_alumno = db.Column(db.Integer, primary_key=True)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    altura = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<ID: {self.id_alumno}, Edad: {self.edad}, Peso: {self.peso}, Altura: {self.altura}> '
    
    def to_json(self):
        alumno_json = {
            'ID': self.id_alumno,
            'EDAD': self.edad,
            'PESO': self.peso,
            'ALTURA': self.altura
            }
        
    @staticmethod
    def from_json(alumno_json):
        id_alumno = alumno_json.get('ID')
        edad = alumno_json.get('EDAD')
        peso = alumno_json.get('PESO')
        altura = alumno_json.get('ALTURA')
        return Alumno(id_alumno=id_alumno,
                      edad=edad,
                      peso=peso,
                      altura=altura
                      )    