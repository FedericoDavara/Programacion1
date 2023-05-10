from .. import db

class Clases(db.Model):
    id_clases = db.Column(db.Integer, primary_key=True)
    horario_clases = db.Column(db.Integer, nullable=True)
    nombre_clases = db.Column(db.String, nullable=False)


    def __repr__(self):
        return f'< Nro° Clase : {self.id_clases},Horario_de_Clases: {self.horario_clases}, Nombre_de_Clases: {self.nombre_clases} '




    def tp_json(self):
        clases_json = {
            'Nro° Clase' : self.id_clases,
            'Horario_de_clases': self.horario_clases,
            'Nombre_de_Clases': self.nombre_clases
        }
        return clases_json
    

    @staticmethod

    def from_json(clases_json):
        id_clases = clases_json.get('Clase_id')
        horario_clases = clases_json.get('Horario_de_clases')
        nombre_clases = clases_json.get('Nombres de clases')
        return Clases(id_clases=id_clases,
                      horario_clases=horario_clases,
                      nombre_clases=nombre_clases
                      )
    

    