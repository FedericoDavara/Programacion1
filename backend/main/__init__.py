from flask import Flask
import os
from dotenv import load_dotenv

#vamos a crear un metodo que inicializara la app y todos los modulos
def create_app():
    #inicio flask
    app = Flask(__name__)
    #variables de entorno
    load_dotenv()
    return app