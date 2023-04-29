from .. import db

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.models.Integer, nullable=False)
    nombre = db.Column(db.models.Varchar(50), nullable=False)
    apellido = db.Column(db.models.Varchar(50), nullable=False)    
    email = db.Column(db.models.Varchar(50), nullable=False)
    telefono = db.Column(db.models.Integer, nullable=False)
    
    def __repr__(self):
        return '<Usuario: %r >' % (self.nombre)
    
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'dni': int(self.nombre),
            'nombre': str(self.nombre),
            'apellido': str(self.nombre),
            'email': str(self.nombre),
            'telefono': int(self.nombre),
        }
        return usuario_json

    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'dni': int(self.nombre),
            'nombre': str(self.nombre),
            'apellido': str(self.nombre),
            'email': str(self.nombre),
            'telefono': int(self.nombre),
        }
        return usuario_json

    @staticmethod
    def from_json(usuario_json):
        id = usuario_json.get('id')
        dni = usuario_json.get('dni')
        nombre = usuario_json.get('nombre')
        apellido = usuario_json.get('apellido')
        email = usuario_json.get('email')
        telefono = usuario_json.get('telefono')
        return Usuario(id=id,
                    dni=dni, 
                    nombre=nombre, 
                    apellido=apellido,
                    email=email,
                    telefono=telefono,
                    )