
#Archivo incio la app
from flask import Flask

app = Flask(__name__)

#Importo todas las rutas de las aplicacion
from . import views