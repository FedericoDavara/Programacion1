from flask_restful import Resource
from flask import request

LOGIN ={
    1:{"usuario:":"carlitos","contrasena":"hola123"}
}

class Login(Resource):
    def post(self):
        login = request.get_json()
        id = int(max(LOGIN.keys()))+1
        LOGIN[id] = login
        return LOGIN[id], 201
