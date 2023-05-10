from .. import db

class Usuarios(db.Model):
    dni = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return (
            f'< DNI: {self.dni}, Nombre: {self.nombre}, Apellido: {self.apellido}, Email: {self.email}, Telefono: {self.telefono}'
        )

    def to_json(self):
        usuarios_json = {
            'DNI': int(self.dni),
            'Nombre': str(self.nombre),
            'Apellidos': str(self.apellido),
            'Email': str(self.email),
            'Telefono': str(self.telefono)
            
        }
        return usuarios_json
    
    @staticmethod
    def from_json(usuario_json):
        dni = usuario_json.get('DNI')
        nombre = usuario_json.get('Nombre')
        apellido = usuario_json.get('Apellido')
        email = usuario_json.get('Email')
        telefono = usuario_json.get('Telefono')
        return Usuarios(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono
            )



