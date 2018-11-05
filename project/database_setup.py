import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()

class Barrio(Base):
	__tablename__ = 'barrio'

	id_barrio = Column(Integer,primary_key=True,autoincrement=True)
	nombre_barrio = Column(String(35),nullable=False)

class Persona(Base):
	__tablename__ = 'persona'

	id_persona = Column(Integer,primary_key=True,autoincrement=True)
	nombre = Column(String(25),nullable=True)
	apellido = Column(String(25),nullable=True)
	telefono = Column(String(30), nullable=True)
	email = Column(String(40),nullable=False)
	foto = Column(String(40),nullable=True)
	pw = Column(String(250), nullable=False)
	id_barrio = Column(Integer,ForeignKey('barrio.id_barrio'),nullable=False)

class Blog(Base):
	__tablename__ = 'blog'

	id_blog = Column(Integer,primary_key=True,autoincrement=True)
	titulo = Column(String(25),nullable=False)
	comentario = Column(String(25),nullable=False)
	fecha_publicacion = Column(DateTime, nullable=False)
	tipo_animal = Column(String(15),nullable=False)
	foto = Column(String(45),nullable=False)
	id_persona = Column(Integer, ForeignKey("persona.id_persona"), nullable=False)



engine = create_engine('postgresql://ezequiel:ezequiel@localhost/dsistemas')
Base.metadata.create_all(engine)

