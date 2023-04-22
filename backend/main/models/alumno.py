from .. import db

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    edad = db.Column(db.Integer, nullable = False)
    peso = db.Column(db.Integer, nullable = False)
    altura = db.Column(db.Integer, nullable = False)
    
    def __repr__(self):
        return '<Alumno : %r %r %r >' % (self.edad, self.peso, self.altura)
    
    def to_json(self):
        alumno_json = {
            'id' : self.id,
            'edad' : int(self.edad),
            'peso' : int(self.peso),
            'altura' : int(self.altura)
            
            
        }
        return alumno_json
    
    def to_json_short(self):
        alumno_json = {
            'id' : self.id,
            'edad' : int(self.edad),
            'peso' : int(self.peso),
            'altura' : int(self.altura)
            
        }
        return alumno_json
    
    @staticmethod
    
    def from_json(alumno_json):
        id = alumno_json.get('id')
        edad = alumno_json('peso')
        peso = alumno_json('peso')
        altura = alumno_json('altura')
        return Alumno(id=id,
                      edad=edad,
                      peso=peso,
                      altura=altura
                      )
        
        
            
            