from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api

import main.resources as resources

api = Api()

def create_app():
    app = Flask(__name__)
    load_dotenv() 
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuariosResource, '/usuario/<id>')
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuariosResource, '/usuario/<id>')
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuariosResource, '/usuario/<id>')
    api.add_resource(resources.PlanificacionAlumnoResource, "/planificacion_a/<id>")
    api.add_resource(resources.PlanificacionProfesorResource,"/planificacion_p/<id>")
    api.add_resource(resources.PlanificacionesProfesoresResources, "/planificaciones_ps")
    api.add_resource(resources.ProfesorClasesResource,"/clases")
    api.add_resource(resources.PagoResource, "/pago/<id>")
    api.add_resource(resources.LoginResource, "/login")
    api.init_app(app)
    return app

