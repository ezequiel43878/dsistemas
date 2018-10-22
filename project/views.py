#Archivo .py con el enrutamiento de la aplicacion..

from . import app
from flask import render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.database_setup import Base

# ----- Pagina de inicio ---------

engine = create_engine('postgresql://ezequiel:ezequiel@localhost/dsistemas')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route ('/')
def index():
	return render_template('index.html')

