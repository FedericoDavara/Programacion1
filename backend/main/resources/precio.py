from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PrecioModel
from flask_jwt_extended import jwt_required
from main.auth.decorators import role_required


class Precio(Resource):
    @jwt_required(optional=True)
    def get(self, id):
        precio = db.session.query(PrecioModel).get_or_404(id)
        return precio.to_json()

    @role_required(roles=["admin"])
    def delete(self, id):
        precio = db.session.query(PrecioModel).get_or_404(id)
        db.session.delete(precio)
        db.session.commit()
        return "", 204

    @role_required(roles=["admin"])
    def put(self, id):
        precio = db.session.query(PrecioModel).get_or_404(id)
        data = request.get_json().items()
        try:
            for key, value in data:
                setattr(precio, key, value)
            db.session.add(precio)
            db.session.commit()
            return precio.to_json(), 200
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": "Error interno del servidor"}, 500


class Precios(Resource):
    @jwt_required(optional=True)
    def get(self):
        precios = db.session.query(PrecioModel).all()
        return jsonify([precio.to_json() for precio in precios])

    @role_required(roles=["admin"])
    def post(self):
        try:
            precio = PrecioModel.from_json(request.get_json())
            db.session.add(precio)
            db.session.commit()
            return precio.to_json(), 201
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": "Error interno del servidor"}, 500
