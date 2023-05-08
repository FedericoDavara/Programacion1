import os
from flask import Flask
from dotenv import load_dotenv

#Importamos nuevas librerias clase 3
from flask_restful import Api #Agrego la clase API

#Importar SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
#Inicializar API de Flask Restful
api = Api()
#Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    #Si no existe el archivo de base de datos crearlo (solo válido si se utiliza SQLite)
    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Url de configuración de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)
    
    import main.resources as resources

    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.UsuarioAlumnoResource, '/usuarioalumno/<id>')
    api.add_resource(resources.UsuariosAlumnosResource, '/usuariosalumnos')
    api.add_resource(resources.UsuarioProfesorResource, '/usuarioprofesor/<id>')
    api.add_resource(resources.PlanificacionAlumnoResource, "/planificacionalumno/<id>")
    api.add_resource(resources.PlanificacionProfesorResource,"/planificacionprofesor/<id>")
    api.add_resource(resources.PlanificacionesProfesoresResources, "/planificacionesprofesores")
    api.add_resource(resources.PagoResource, "/pago/<id>")
    api.add_resource(resources.LoginResource, "/login")
    
    api.init_app(app)
    
    return app

