from .. import db

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.models.String(20), nullable=False)
    contraseña = db.Column(db.models.String(20), nullable=False)
    
    def __repr__(self):
        return '<login: %r >' % (self.nombre_usuario)
    
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre_usuario': str(self.nombre_usuario),
            'contraseña': str(self.contraseña)
        }
        return usuario_json

    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'nombre_usuario': str(self.nombre_usuario),
            'contraseña': str(self.contraseña),
        }
        return usuario_json

    @staticmethod
    def from_json(login_json):
        id = login_json.get('id')
        nombre_usuario = login_json.get('nombre_usuario')
        contraseña = login_json.get('contraseña')

        return Login(id=id,
                    nombre_usuario=nombre_usuario, 
                    contraseña=contraseña, 
                    )