from flask import Flask, request, flash, redirect, url_for, render_template
from router import routers as rt
import pymysql
from pymysql.cursors import DictCursor
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)
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


if __name__ == '__main__':
    app.run(debug=True)
