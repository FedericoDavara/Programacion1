import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


api = Api()
db=SQLAlchemy()
migrate = Migrate()

#metodo que inicializa la app y todos los modulos

def create_app():

    app = Flask(__name__)
    load_dotenv()

    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Url de configuración de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)
    migrate.init_app(app,db)
    
    #Importar directorio de recursos
    import main.resources as resources

    api.add_resource(resources.UsuariosResource,"/usuarios")

    api.add_resource(resources.UsuarioResource, "/usuario/<dni>")

    api.add_resource(resources.UsuariosAlumnosResource, "/usuarios_alumnos")

    api.add_resource(resources.UsuarioAlumnoResource, "/usuario_alumno/<dni>")

    api.add_resource(resources.UsuariosProfesoresResource, "/usuarios_profesores")

    api.add_resource(resources.UsuarioProfesorResource, "/usuario_profesor/<dni>")

    api.add_resource(resources.PlanificacionesResource, "/planificaciones")

    api.add_resource(resources.PlanificacionResource, "/planificacion/<id>")

    api.add_resource(resources.PlanificacionAlumnoResource, "/planificacion_alumno/<dni>")

    api.add_resource(resources.PlanificacionProfesorResource,"/planificacion_profesor/<dni>")

    api.add_resource(resources.PlanificacionesProfesoresResource, "/planificaciones_profesores")

    api.add_resource(resources.ClasesResource,"/clases")

    api.add_resource(resources.ClaseResource,"/clase/<id>")

    api.add_resource(resources.PagoResource, "/pago/<id>")

    api.add_resource(resources.LoginResource, "/login")

    api.init_app(app)


    #retornamos la app inicializada
    return app