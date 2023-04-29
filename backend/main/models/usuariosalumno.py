from .. import db

class UsuarioAlumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Interger, nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<UsuarioAlumno : %r %r %r >' % (self.edad, self.peso, self.altura)
    
    def to_json(self):
        usuarioalumno_json = {
            'id' : self.id,
            'edad' : int(self.edad),
            'peso' : int(self.peso),
            'altura' : int(self.altura)
            
            
        }
        return usuarioalumno_json
    
    def to_json_short(self):
        usuarioalumno_json = {
            'id' : self.id,
            'edad' : int(self.edad),
            'peso' : int(self.peso),
            'altura' : int(self.altura)
            
        }
        return usuarioalumno_json
    
    @staticmethod
    
    def from_json(usuarioalumno_json):
        id = usuarioalumno_json.get('id')
        edad = usuarioalumno_json('peso')
        peso = usuarioalumno_json('peso')
        altura = usuarioalumno_json('altura')
        return UsuarioAlumno(id=id,
                      edad=edad,
                      peso=peso,
                      altura=altura
                      )