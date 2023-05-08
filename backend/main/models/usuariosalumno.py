from .. import db
from . import UsuarioModel

class UsuarioAlumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
    usuario = db.relationship("Usuarios", uselist=False, back_populates="alumnos",cascade="all, delete-orphan", single_parent=True)

    def __repr__(self):
        return '<UsuarioAlumno : %r %r %r %r >' % (self.usuario_id, self.edad, self.peso, self.altura)
    
    def to_json(self):
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.usuario_id)
        usuarioalumno_json = {
            'id' : self.id,
            'edad' : int(self.edad),
            'peso' : int(self.peso),
            'altura' : int(self.altura),
            'usuario' : self.usuario.to_json()
            
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
        usuario_id = usuarioalumno_json('usuario_id')
        return UsuarioAlumno(id=id,
                      edad=edad,
                      peso=peso,
                      altura=altura,
                      usuario_id=usuario_id
                      )