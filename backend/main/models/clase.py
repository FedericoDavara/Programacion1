from .. import db, sa
import datetime

profesor_clases = db.Table("profesor_clases",
   sa.Column("id_profesor",db.Integer,db.ForeignKey("profesor.id_profesor")),
   sa.Column("id_clase",db.Integer,db.ForeignKey("clases.id")), 
   extend_existing = True    
  )


class Clase(db.Model):
    clase_id = sa.Column(db.Integer, primary_key = True)
    horario = sa.Column(db.String(100),nullable = False)
    nombre = sa.Column(db.String(100),nullable = False)
    dia = sa.Column(db.String(100),nullable = False)
    profesor = db.relationship('Profesor', secondary=profesor_clases, 
                               backref = db.backref('clases', lazy='dynamic'))

    


    def __repr__(self):
        return (f'<Clase_id: {self.clase_id}, Horario: {self.horario}, '+ 
        f'Nombre: {self.nombre}, Dia: {self.dia}>')     
    def to_json(self):
        clases_json = {
            'Clase_id' : self.id,
            'Horario' : str(self.horario),
            'Nombre' : str(self.nombre),
            'Dia' : str(self.dia)
        }
        return clases_json
    
    def to_json_complete(self):
        clase_json = {
            'Clase_id' : self.clase_id,
            'Horario': self.horario,
            'Nombre': self.nombre,
            'Dia': self.dia,
            "Profesores": [profesor.to_json() for profesor in self.profesores]
        }
        return clase_json



    @staticmethod

    def from_json(clase_json):
        return Clase(clase_id = clase_json.get('Clase_id'),
                      nombre = clase_json.get('Nombre'),
                      horario = datetime.strptime(clase_json.get("horario"), "%H:%M")
                      )
    

    