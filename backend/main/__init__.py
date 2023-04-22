import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import main.resources as resources

api = Api()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    if not os.path.exists(os.getenv('DATABASE_PATH')+ os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+ os.getenv("DATABASE_NAME"))
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    import main.resources as resources    
    
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.UsuarioAlumnoResource, '/usuarioalumno')
    api.add_resource(resources.UsuariosAlumnosResource, '/usuariosalumnos/<id>')
    api.add_resource(resources.UsuarioProfesorResource, '/usuarioprofesor/<id>')
    api.add_resource(resources.PlanificacionAlumnoResource, "/planificacion_a/<id>")
    api.add_resource(resources.PlanificacionProfesorResource,"/planificacion_p/<id>")
    api.add_resource(resources.PlanificacionesProfesoresResources, "/planificaciones_ps")
    api.add_resource(resources.ProfesorClasesResource,"/clases")
    api.add_resource(resources.PagoResource, "/pago/<id>")
    api.add_resource(resources.LoginResource, "/login")
    api.init_app(app)
    return app

