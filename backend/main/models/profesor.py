from .. import db

class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = False)
    especialidad = db.Column(db.String(100), nullalble = False)

    def __repr__(self):
        return '<Profesor : %r %r >' & (self.titulo, self.especialidad)
    
    def to_json(self):
        profesor_json = {
            'id' : self.id,
            'titulo' : str(self.titulo),
            'especialidad' : str(self.especialidad)
            
        }
        return profesor_json
    
    def to_json_short(self):
        profesor_json = {
            'id' : self.id,
            'titulo' : str(self.titulo),
            'especialidad' : str(self.especialidad)
            
        }
        return profesor_json
    
    @staticmethod
    def from_json(profesor_json):
        id = profesor_json.get('id')
        titulo = profesor_json.get('titulo')
        especialidad = profesor_json.get('especialidad')
        return Profesor(id=id,
                        titulo=titulo,
                        especialidad=especialidad
                        )
        
        
        