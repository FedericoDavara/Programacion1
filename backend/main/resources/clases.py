
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ClaseModel, AlumnoModel, ProfesorModel
from datetime import datetime
import regex
    
class Clase(Resource):
    def get(self, id):
        clase = db.session.query(ClaseModel).get_or_404(id)
        return clase.to_json_complete()

    def put(self, id):
        clase = db.session.query(ClaseModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            if regex.match(r"\d{2}:\d{2}", str(value)) != None:
                setattr(clase, key.lower(), datetime.strptime(value, "%H:%M"))
            else: setattr(clase, key.lower(), value)
        db.session.add(clase)
        db.session.commit()
        return clase.to_json(), 201        

    def delete(self, id):
        clase = db.session.query(ClaseModel).get_or_404(id)
        db.session.delete(clase)
        db.session.commit()
        return '', 204
    
class Clases(Resource):
    def get(self):
        clases = db.session.query(ClaseModel).all()
        return jsonify([clase.to_json() for clase in clases])

    def post(self):
        try:
            clase = ClaseModel.from_json(request.get_json())
        except:
            return 'Formato no correcto', 400
        db.session.add(clase)
        db.session.commit()
        return clase.to_json(), 201
    
class ClasesAlumnos(Resource):
    def post(self, id, dni):
        alumno = db.session.query(AlumnoModel).get_or_404(dni)
        clase = db.session.query(ClaseModel).get_or_404(id)
        alumno.clases.append(clase)
        db.session.commit()
        return alumno.to_json_complete(), 201
    
    def delete(self, id, dni):
        alumno = db.session.query(AlumnoModel).get_or_404(dni)
        clase = db.session.query(ClaseModel).get_or_404(id)
        alumno.clases.remove(clase)
        db.session.commit()
        return '', 204

class ClasesProfesores(Resource):
    def post(self, id, dni):
        profesor = db.session.query(ProfesorModel).get_or_404(dni)
        clase = db.session.query(ClaseModel).get_or_404(id)
        profesor.clases.append(clase)
        db.session.commit()
        return profesor.to_json_complete(), 201

    def delete(self, id, dni):
        profesor = db.session.query(ProfesorModel).get_or_404(dni)
        clase = db.session.query(ClaseModel).get_or_404(id)
        profesor.clases.remove(clase)
        db.session.commit()
        return '', 204
    
