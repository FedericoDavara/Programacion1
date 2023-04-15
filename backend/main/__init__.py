from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api

import main.resources as resources

api = Api()

def create_app():
    app = Flask(__name__)
    load_dotenv() 
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.UsuarioAlumnoResource, '/usuarioalumno/<id>')
    api.add_resource(resources.UsuariosAlumnosResource, '/usuariosalumnos')
    api.add_resource(resources.UsuarioProfesorResource, '/usuarioprofesor/<id>')
    api.add_resource(resources.PlanificacionAlumnoResource, "/planificacionalumno/<id>")
    api.add_resource(resources.PlanificacionProfesorResource,"/planificacionprofesor/<id>")
    api.add_resource(resources.PlanificacionesProfesoresResources, "/planificacionesprofesores")
    api.add_resource(resources.ProfesorClasesResource,"/clases")
    api.add_resource(resources.PagoResource, "/pago/<id>")
    api.add_resource(resources.LoginResource, "/login")
    api.init_app(app)
    return app

