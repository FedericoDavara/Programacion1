from .. import db
from . import ProfesorModel

profesor_clases = db.Table("profesor_clases",
    db.Column("profesor_id",db.Integer,db.ForeignKey("profesor.id"),primary_key=True),
    db.Column("id_clase",db.Integer,db.ForeignKey("clases.id"),primary_key=True)   
    )

class Clases(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    horario = db.Column(db.Strin(100),nullable = False)
    nombre = db.Column(db.Strin(100),nullable = False)
    dia = db.Column(db.Strin(100),nullable = False)
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
    
    def to_json_short(self):
        clases_json = {
            'id' : self.id,
            'horario' : str(self.horario),
            'nombre' : str(self.nombre),
            'dia' : str(self.dia)
        }
        return clases_json
    
       
    
    @staticmethod
    def from_json(clases_json):
        id = clases_json.get('id')
        horario = clases_json.get('horario')
        nombre = clases_json.get('nombre')
        dia = clases_json.get('dia')
        return Clases(id=id,
                      horario=horario,
                      nombre=nombre,
                      dia=dia
                      )
        
    