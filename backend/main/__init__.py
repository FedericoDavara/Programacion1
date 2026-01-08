import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail


api = Api()
db=SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mailsender = Mail()
#metodo que inicializa la app y todos los modulos

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Construcción segura de la ruta de la base de datos
    db_path = os.getenv('DATABASE_PATH')
    db_name = os.getenv('DATABASE_NAME')
    full_db_path = os.path.join(db_path, db_name)

    # Configuración de base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{full_db_path}'
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configuración JWT - Convertir a int el tiempo de expiración
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    # Configuración de Mail con conversiones de tipos
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    # Convertir el string "True" a un booleano real
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() in ['true', '1', 't']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    
    mailsender.init_app(app)
    
    #Importar directorio de recursos
    import main.resources as resources

    api.add_resource(resources.UsuariosResource,"/usuarios")

    api.add_resource(resources.UsuarioResource, "/usuario/<dni>")

    api.add_resource(resources.UsuariosAlumnosResource, "/usuarios_a")

    api.add_resource(resources.UsuarioAlumnoResource, "/usuario_a/<dni>")

    api.add_resource(resources.UsuariosProfesoresResource, "/usuarios_p")

    api.add_resource(resources.UsuarioProfesorResource, "/usuario_p/<dni>")

    api.add_resource(resources.PlanificacionesResource, "/planificaciones")

    api.add_resource(resources.PlanificacionResource, "/planificacion/<id>")

    api.add_resource(resources.PlanificacionAlumnoResource, "/planificacion_a/<dni>")

    api.add_resource(resources.PlanificacionProfesorResource,"/planificacion_p/<dni>")

    api.add_resource(resources.PlanificacionesProfesoresResource, "/planificaciones_ps")

    api.add_resource(resources.ClasesResource,"/clases")

    api.add_resource(resources.ClaseResource,"/clase/<id>")

    api.add_resource(resources.PermisosResource,"/permisos")

    api.add_resource(resources.PermisoResource,"/permiso/<id>")


    #api.add_resource(resources.PagoResource, "/pago/<id>")

    #api.add_resource(resources.LoginResource, "/login")

    api.init_app(app)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    from main.auth import routes
    app.register_blueprint(routes.auth)

  #Configuración de mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    #Inicializar en app
    mailsender.init_app(app)

    #retornamos la app inicializada
    return app