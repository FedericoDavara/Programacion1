import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
api = Api()
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    
    load_dotenv() 
    import main.resources as resources
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.UsuarioAlumnoResource, '/usuarioalumno/<id>')
    api.add_resource(resources.UsuariosAlumnosResource, '/usuariosalumnos')
    api.add_resource(resources.UsuarioProfesorResource, '/usuarioprofesor/<id>')
    api.add_resource(resources.PlanificacionAlumnoResource, "/planificacionalumno/<id>")
    api.add_resource(resources.PlanificacionProfesorResource,"/planificacionprofesor/<id>")
    api.add_resource(resources.ProfesorClasesResource,"/clases")
    api.add_resource(resources.PagoResource, "/pago/<id>")
    api.add_resource(resources.LoginResource, "/login")
    
    
    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)
    api.init_app(app)
    with app.app_context():
        db.create_all()
    return app

