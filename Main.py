from flask import Flask, request, flash, redirect, url_for, render_template
from router import routers as rt
import pymysql
from pymysql.cursors import DictCursor
import os
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24) #llave random para que funcione ALV 



# Configuración de la base de datos
DB_CONFIG = {
    'host': "by8ekzvhusvvn2yqc71b-mysql.services.clever-cloud.com",
    'user': "uueyyhu8xg3oenlv",
    'password': "VFbwWo8TNmZQbg04Dd7i",
    'database': "by8ekzvhusvvn2yqc71b",
    'cursorclass': DictCursor
}

def get_db_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except pymysql.Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        return None

def db_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = get_db_connection()
        if not conn:
            flash("No se pudo conectar a la base de datos.", "danger")
            return redirect(url_for('home'))
        try:
            with conn.cursor() as cursor:
                result = func(cursor, *args, **kwargs)
            conn.commit()
            return result
        except pymysql.Error as e:
            conn.rollback()
            flash(f"Error en la base de datos: {e}", 'danger')
        finally:
            conn.close()
    return wrapper

@app.route('/')
@app.route('/home')
def home_route():
    return rt.home()  # Llama a la función home desde router


# UN PEDAZO DE CACA >>>>> PAWECHA 🧐

@app.route('/padres', methods=['GET', 'POST'])
@db_operation
def padres_router(cursor):
    if request.method == 'POST':
        nombre = request.form['nombre']
        numero = request.form['numero']
        correo = request.form['correo']
        dui = request.form['dui'] 

        try:
            cursor.execute(
                "INSERT INTO padres (nombre, numero, correo, dui) VALUES (%s, %s, %s, %s)",
                (nombre, numero, correo, dui)
            )
            flash('Padre registrado con éxito.', 'success')
        except Exception as e:
            flash(f'Error al registrar Padre: {e}', 'danger')

        return redirect(url_for('padres_router')) 

    return render_template('/padres.html')



@app.route('/secciones', methods=['GET', 'POST'])
@db_operation
def secciones_router(cursor):
    if request.method == 'POST':
        seccion = request.form['seccion']
        año = request.form['año']
        especialidad = request.form['especialidad']
 
        try:
            cursor.execute(
                #                *Se la INSERTA >~<*
                "INSERT INTO seccion (seccion, año, especialidad ) VALUES (%s, %s, %s)",
                (seccion, año, especialidad)
                )
            flash('alumno registrado con éxito. ', 'success')
        except Exception as e:
            flash(f'Error al registrar alumno: {e}', 'danger')
            
        return redirect(url_for('secciones_router')) 

    return render_template('/secciones.html')


@app.route('/estudiantes', methods=['GET', 'POST'])
@db_operation
def estudiantes_router(cursor):
    if request.method == 'POST':
        nombre = request.form['nombre']
        nie = request.form['nie']
        edad = request.form['edad']
        año = request.form['año']
        codigo = request.form['codigo']

        try:
            cursor.execute(
                #            *Se la INSERTA >~<*
                "INSERT INTO estudiantes (nombre, nie, edad, año, codigo) VALUES (%s, %s, %s, %s, %s)",
                (nombre, nie, edad, año, codigo)
                )
            flash('alumno registrado con éxito. ', 'success')
        except Exception as e:
            flash(f'Error al registrar alumno: {e}', 'danger')
            
        return redirect(url_for('estudiantes_router')) 

    return render_template('/estudiantes.html')


@app.route('/asistencia', methods=['GET', 'POST'])
@db_operation
def asistencia_router(cursor):
    if request.method == 'POST':
        nie_estudiante = request.form['nie']
        
        try:
            # Verifica si el estudiante existe
                        
            cursor.execute("SELECT * FROM estudiantes WHERE nie = %s", (nie_estudiante,))
            estudiante = cursor.fetchone()
            
            if estudiante:
                # Registrar asistencia
                fecha_actual = datetime.now().date()
                hora_actual = datetime.now().time()
                cursor.execute(
                    #              *Se la INSERTA >~<*
                    "INSERT INTO entrada (nie, data, hour) VALUES (%s, %s, %s)",
                    (nie_estudiante, fecha_actual, hora_actual)
                )
                connection.commit() 

                flash('Asistencia registrada con éxito.', 'success')
            else:
                flash('El estudiante con ese NIE no existe.', 'danger')
        
        except Exception as e:
            flash(f'Ocurrió un error: {str(e)}', 'danger')
        
        return redirect(url_for('asistencia_router')) 

    return render_template('/asistencia.html')


@app.route('/salida', methods=['GET', 'POST'])
@db_operation
def salida_router(cursor):
    if request.method == 'POST':
        nie_estudiante = request.form['nie']
        
        try:
            # Verificar si el estudiante existe
            cursor.execute("SELECT * FROM estudiantes WHERE nie = %s", (nie_estudiante,))
            estudiante = cursor.fetchone()
            
            if estudiante:
                # Registrar asistencia
                fecha_actual = datetime.now().date()
                hora_actual = datetime.now().time()
                cursor.execute(

                            #*Se la INSERTA >~<*
                    "INSERT INTO salida (nie, data, hour) VALUES (%s, %s, %s)",
                    (nie_estudiante, fecha_actual, hora_actual)
                )
                connection.commit() 


                flash('Asistencia registrada con éxito.', 'success')
            else:
                flash('El estudiante con ese NIE no existe.', 'danger')
        
        except Exception as e:
            flash(f'Ocurrió un error: {str(e)}', 'danger')
        
        return redirect(url_for('salida_router')) 

    return render_template('/salida.html')

if __name__ == '__main__':
    app.run(debug=True)
