from flask import render_template
from backend import db as db

#crea la conexion con la base de datos ajustar a los que necesites esta es para xampp
db = db(host="localhost", user="root", password="", database="pruebafullh")

#crea la conexion con la base de datos
#db = db(host="localhost", user="tu_usuario", password="tu_password", database="nombre_base_datos")

def home():
    web_name: str = 'Home'
    return render_template('index.html', web_name=web_name)
def padres():
    web_name: str = 'Registro de Padres'
    return render_template('padres.html', web_name=web_name)

def estudiantes():
    web_name: str = 'Registro de Alumnos'
    return render_template('estudiantes.html', web_name=web_name)

def secciones():
    web_name: str = 'Registro de Secciones'
    return render_template('secciones.html', web_name=web_name)

def asistencia():
    web_name: str = 'Registro de Asistencia'
    return render_template('asistencia.html', web_name=web_name)

def salida():
    web_name: str = 'Registro de salida'
    return render_template('salida.html', web_name=web_name)

