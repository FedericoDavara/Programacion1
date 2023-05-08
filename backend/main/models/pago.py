from .. import db

class Clases(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pago = db.Column(db.String(100),nullable = False)

    
    def __repr__(self):
        return '<Clases : %r %r %r >' & (self.pago)
    
    def to_json(self):
        clases_json = {
            'id' : self.id,
            'pago' : str(self.pago)
        }
        return clases_json
    
    def to_json_short(self):
        clases_json = {
            'id' : self.id,
            'horario' : str(self.horario),
            'pago' : str(self.pago)
        }
        return clases_json
    
       
    
    @staticmethod
    def from_json(clases_json):
        id = clases_json.get('id')
        pago = clases_json.get('pago')
        return Clases(id=id,
                      pago=pago
                      )
        
    