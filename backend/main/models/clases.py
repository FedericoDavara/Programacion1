from .. import db, sa

profesor_clases = db.Table("profesor_clases",
   sa.Column("id_profesor",db.Integer,db.ForeignKey("profesor.id_profesor")),
   sa.Column("id_clase",db.Integer,db.ForeignKey("clases.id")), 
   extend_existing = True    
  )


class Clases(db.Model):
    id = sa.Column(db.Integer, primary_key = True)
    horario = sa.Column(db.String(100),nullable = False)
    nombre = sa.Column(db.String(100),nullable = False)
    dia = sa.Column(db.String(100),nullable = False)
    profesor = db.relationship('Profesor', secondary=profesor_clases, backref=db.backref('clases', lazy='dynamic'))

    


    def __repr__(self):
        return '<Clases : %r %r %r >' & (self.horario, self.nombre, self.dia)
    
    def to_json(self):
        clases_json = {
            'id' : self.id,
            'horario' : str(self.horario),
            'nombre' : str(self.nombre),
            'dia' : str(self.dia)
        }
        return clases_json
    
    def to_json_complete(self):
        clase_json = {
            'Nro° Clase' : self.id,
            'Horario_de_clases': self.horario,
            'Nombre_de_Clases': self.nombre,
            'Dia': self.dia,
            "Profesores": [profesor.to_json() for profesor in self.profesores]
        }
        return clase_json



    @staticmethod

    def from_json(clases_json):
        return Clases(id=clases_json.get('Clase_id'),
                      horario=clases_json.get('Horario_de_clases'),
                      nombre=clases_json.get('Nombres de clases')
                      )
    

    