from .. import db
from . import UsuarioModel

class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = False)
    especialidad = db.Column(db.String(100), nullalble = False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
    usuario = db.relationship("Usuarios", uselist=False, back_populates="profesores",cascade="all, delete-orphan", single_parent=True)
  
    def __repr__(self):
        return '<Profesor : %r %r %r >' & (self.usuario_id, self.titulo, self.especialidad)
    
    def to_json(self):
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.usuario_id)
        profesor_json = {
            'id' : self.id,
            'titulo' : str(self.titulo),
            'especialidad' : str(self.especialidad),
            'usuario' : self.usuario.to_json() 
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
        usuario_id = profesor_json.get('usuario_id')
        return Profesor(id=id,
                        titulo=titulo,
                        especialidad=especialidad,
                        usuario_id=usuario_id
                        )

