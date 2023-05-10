from .. import db

class Profesor(db.Model):
    id_profesor = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return (
            f'<ID: {self.id_profesor}, Titulo: {self.titulo},Especialidad{self.especialidad}'
        )
    
    def to_json(self):
        profesor_json = {
            'ID': int(self.id_profesor),
            'Titulo': str(self.titulo),
            'Especialidad': str(self.especialidad) 
        }
        return profesor_json
    
    @staticmethod
    def from_json(usuario_json):
        id_profesor = usuario_json.get('ID')
        titulo = usuario_json.get('Titulo')
        especialidad = usuario_json.get('especialidad')
        return Profesor(
            id_profesor=id_profesor,
            titulo=titulo,
            especialidad=especialidad

        )        