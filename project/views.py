#Archivo .py con el enrutamiento de la aplicacion..

from . import app
from flask import render_template, request, redirect, url_for
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.database_setup import Base, Persona, Barrio
import hashlib
import random
import string
from werkzeug.utils import secure_filename
import os

# Carpeta donde se guardan las imagenes

UPLOAD_FOLDER = 'project/static/imagenes'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#Funciones de hasheo de contraseña

def make_salt():
	return ''.join(random.choice(
				string.ascii_uppercase + string.digits) for x in range(32))
		
def make_pw_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256((name + pw + salt).encode('utf-8')).hexdigest()
	return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
	salt = h.split(',')[0]
	return h == make_pw_hash(name, password, salt)

# ----- Pagina de inicio ---------

engine = create_engine('postgresql://ezequiel:ezequiel@localhost/dsistemas')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# -------- Registrar ---
@app.route('/registrar',methods=['POST','GET'])
def registar():
	if not 'username' in login_session:
		if request.method == 'GET':
			return render_template('registrar.html')
		else:
			if request.method == 'POST':
				email = request.form['email'].lower()
				pw = request.form['pass']
				pw2 = request.form['pass2']
				registro = session.query(Persona).all()
				existe_email = False
				if pw == pw2:
					for x in registro:
						if x.email == email:
							existe_email = True
							break
					if existe_email == False:
						pw_hash = make_pw_hash(email,pw)
						nuevo_usuario = Persona(
							email = email,
							pw = pw_hash,
							id_barrio = 1,
							foto = 'sin_foto.png'
							)
						print (email)
						session.add(nuevo_usuario)
						session.commit()
						login_session['username'] = email
						return redirect(url_for('edit_user'))
					else:
						return 'Ya existe un Registro con ese email'
				else:
					return 'contraseña no son iguales'
	else:
		return redirect(url_for('index'))

# -------- Login -----
@app.route('/login',methods=['POST','GET'])
def login():
	if not 'username' in login_session:
		if request.method == 'GET':
			return render_template('login.html')

		else:
			if request.method == 'POST':
				email = request.form['email'].lower()
				pw2 = request.form['pass']
				registro = session.query(Persona).all()
				for x in registro:
					if x.email == email:
						if x and valid_pw(email,pw2,x.pw):
							login_session['username'] = email
							login_session['foto_perfil'] = x.foto
							print('datos correctos')
							return redirect(url_for('index'))
				return 'datos incorrectos'
	else:
		return redirect(url_for('index'))

# --------- Salir ---------

@app.route('/logout')
def logout():
		
		del login_session['username']
		return redirect(url_for('index'))


@app.route('/edit_user',methods=['POST','GET'])
def edit_user():
	if 'username' in login_session:
		email = login_session['username']
		registro = session.query(Persona).filter_by(email = email).one()
		if request.method == 'GET':			
			barrios = session.query(Barrio).all()
			barrio_del_usuario = session.query(Barrio).join(Persona).filter_by(email = email).one()
			return render_template('edit_user.html',username = login_session['username'],registro = registro,barrios = barrios,b2 = barrio_del_usuario )
		else:
			if 'imagen' in request.files:
				file = request.files['imagen']
				if file and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					file.save(os.path.join(UPLOAD_FOLDER, filename))
					registro.foto = filename
			registro.apellido =request.form['apellido']
			registro.nombre = request.form['nombre']
			registro.telefono = request.form['telefono']
			registro.id_barrio = request.form['barrio']
			session.commit()

			return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))

# --------- Index -------
@app.route ('/',methods=['POST','GET'])
def index():
	if 'username' in login_session:
		return render_template('index.html',username = login_session['username'], foto_perfil= login_session['foto_perfil'])
	else:
		return render_template('index.html')
