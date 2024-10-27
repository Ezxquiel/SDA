from flask import render_template

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

