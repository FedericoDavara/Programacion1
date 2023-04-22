from .. import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    dni = db.Column(db.Integer, nullable = False)
    nombre = db.Column(db.String(100), nullable = False)
    apellido = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    telefono = db.Column(db.Integer, nullable = False)
    
    def __repr__(self):
        return '<Usuarios : %r %r %r %r %r %r >' % (self.dni, self.nombre, self.apellido, self.email, self.telefono)
    
    def to_json(self):
        usuario_json = {
            'id' : self.id,
            'dni' : int(self.dni),
            'nombre' : str(self.nombre),
            'apellido' : str(self.apellido),
            'email' : str(self.email),
            'telefono' : int(self.telefono)
            
        }
        return usuario_json
    
    def to_json_short(self):
        usuario_json = {
            'id' : self.id,
            'dni' : int(self.dni),
            'nombre' : str(self.nombre),
            'apellido' : str(self.apellido),
            'email' : str(self.email),
            'telefono' : int(self.telefono)
            
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