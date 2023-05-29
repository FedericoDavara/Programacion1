from .. import db, sa


class Usuarios(db.Model):
    dni = sa.Column(sa.Integer, primary_key=True)
    nombre = sa.Column(sa.String(100), nullable=False)
    apellido = sa.Column(sa.String(100), nullable=False)
    email = sa.Column(sa.Integer, nullable=False)
    telefono = sa.Column(sa.Integer, nullable=False)
    profesor = db.relationship("Profesor", uselist = False, back_populates= "usuario",
                               cascade="all, delete-orphan", single_parent = True)
    alumno = db.relationship("Alumno", uselist = False, back_populates = "usuario", 
                              cascade = "all, delete-orphan", single_parent = True)


    def __repr__(self):
        return (
            f'<DNI: {self.dni}, Nombre: {self.nombre}, Apellido: {self.apellido}, Email: {self.email}, Telefono: {self.telefono}'
        )

    def to_json(self):
        usuarios_json = {
            
            'DNI': int(self.dni),
            'Nombre': str(self.nombre),
            'Apellido': str(self.apellido),
            'Email': str(self.email),
            'Telefono': str(self.telefono)
            
        }
        return usuarios_json

    def to_json_complete(self):
        if self.alumno != None:
            roltxt = "Alumno"
            roljson = self.alumno.to_json()
        elif self.profesor != None:
            roltxt = "Profesor"
            roljson = self.profesor.to_json()
        else: roltxt, roljson = "", ""
        usuario_json = {
            "Nombre": str(self.nombre),
            "Apelidos": str(self.apellidos),
            "Telefono": str(self.telefono),
            "Email": str(self.email),
            "Estado": bool(self.estado),
            roltxt: roljson
        }
        return usuario_json

    @staticmethod
    def from_json(usuario_json):
        return Usuarios(
            
            dni=usuario_json.get('DNI'),
            nombre=usuario_json.get('Nombre'),
            apellido=usuario_json.get('Apellido'),
            email= usuario_json.get('Email'),
            telefono=usuario_json.get('Telefono')
            )



