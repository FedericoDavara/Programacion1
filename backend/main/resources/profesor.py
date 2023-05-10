from flask_restful import Resource
from flask import request

PROFESORES = {
    1: {"profesor":"Martin Demichellis ","clase":"YOGA"},
    2: {"profesor":"Roman Riquelme ","clase":"CALISTENIA"}
}

class ProfesorClases(Resource):
     def get(self):
        return PROFESORES
    
    