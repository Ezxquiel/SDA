from multiprocessing.dummy import connection
from flask import Flask, request, flash, redirect, url_for, render_template
from router import routers as rt
import pymysql
from pymysql.cursors import DictCursor
import os
from functools import wraps
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from flask import make_response
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
    return rt.home()  # Llamamos a la función home desde router


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
    # Fetch available DUIs, sections, and years to populate the form
    cursor.execute("SELECT dui FROM padres")  # Fetch DUIs from parents
    duis = [row['dui'] for row in cursor.fetchall()]  # Using DictCursor

    cursor.execute("SELECT seccion FROM seccion")  # Fetch sections
    secciones = [row['seccion'] for row in cursor.fetchall()]  # Using DictCursor

    cursor.execute("SELECT DISTINCT año FROM seccion")  # Fetch distinct years
    anios = [row['año'] for row in cursor.fetchall()]  # Using DictCursor

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form['nombre']
            nie = request.form['nie']
            edad = request.form['edad']
            año = request.form['año']
            codigo = request.form['codigo']
            dui = request.form['dui']
            seccion = request.form['seccion']

            # Verificar si el padre existe
            cursor.execute("SELECT * FROM padres WHERE dui = %s", (dui,))
            padre = cursor.fetchone()
            if not padre:
                flash('El DUI del padre no está registrado.', 'danger')
                return redirect(url_for('estudiantes_router'))
            
            # Verificar si la sección existe
            cursor.execute("SELECT * FROM seccion WHERE seccion = %s AND año = %s", 
                           (seccion, año))
            seccion_exists = cursor.fetchone()
            if not seccion_exists:
                flash('La sección o año especificado no existe.', 'danger')
                return redirect(url_for('estudiantes_router'))

            # Insertar estudiante
            cursor.execute("""
                INSERT INTO estudiantes 
                (nombre, nie, edad, año, codigo, dui, seccion) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, nie, edad, año, codigo, dui, seccion))
            
            flash('Alumno registrado con éxito.', 'success')
            
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:  # Error de duplicado
                flash('Error: El NIE ya está registrado.', 'danger')
            else:
                flash(f'Error en la base de datos: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
            
        return redirect(url_for('estudiantes_router')) 

    return render_template('estudiantes.html', duis=duis, secciones=secciones, anios=anios)



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
                    "INSERT INTO entrada (nie, fecha, hora) VALUES (%s, %s, %s)",
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
                    "INSERT INTO salida (nie, fecha, hora) VALUES (%s, %s, %s)",
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

def generar_pdf(asistencias):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    p.drawString(100, height - 100, "Reporte de Asistencias")

    # Table headers
    x_offset = 50
    y_offset = height - 150
    line_height = 20
    headers = ["Nombre", "Código", "NIE", "Fecha", "Hora"]
    for i, header in enumerate(headers):
        p.drawString(x_offset + i * 100, y_offset, header)
    y_offset -= line_height

    # Table rows
    for asistencia in asistencias:
        for i, item in enumerate(asistencia):
            p.drawString(x_offset + i * 100, y_offset, str(item))
        y_offset -= line_height

    p.showPage()
    p.save()
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename="asistencias.pdf"'
    return response

@app.route('/administracion', methods=['GET', 'POST'])
def administracion():
    conn = get_db_connection()
    if not conn:
        flash("No se pudo conectar a la base de datos.", "danger")
        return render_template('administracion.html', asistencias_hoy=[], salidas_hoy=[])

    asistencias_hoy = []
    salidas_hoy = []
    busqueda = ''
    fecha_inicio = ''
    fecha_fin = ''

    if request.method == 'POST':
        busqueda = request.form.get('busqueda', '').strip()
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        descargar_pdf = request.form.get('descargar_pdf')

        # Usar la fecha actual si no se ingresan fechas
        fecha_inicio = fecha_inicio if fecha_inicio else datetime.now().date()
        fecha_fin = fecha_fin if fecha_fin else datetime.now().date()

        try:
            with conn.cursor() as cursor:
                # Consulta para entradas
                cursor.execute(
                    """SELECT 
                        e.nombre, 
                        e.codigo, 
                        e.nie, 
                        ent.fecha,
                        ent.hora 
                    FROM entrada ent
                    JOIN estudiantes e ON ent.nie = e.nie 
                    WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                    AND ent.fecha BETWEEN %s AND %s
                    ORDER BY ent.fecha DESC, ent.hora DESC""",
                    ('%' + busqueda + '%', '%' + busqueda + '%', fecha_inicio, fecha_fin)
                )
                asistencias_hoy = cursor.fetchall()
                
                # Consulta para salidas
                cursor.execute(
                    """SELECT 
                        e.nombre, 
                        e.codigo, 
                        e.nie, 
                        sal.fecha,
                        sal.hora
                    FROM salida sal
                    JOIN estudiantes e ON sal.nie = e.nie 
                    WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                    AND sal.fecha BETWEEN %s AND %s
                    ORDER BY sal.fecha DESC, sal.hora DESC""",
                    ('%' + busqueda + '%', '%' + busqueda + '%', fecha_inicio, fecha_fin)
                )
                salidas_hoy = cursor.fetchall()

                print("Asistencias encontradas:", asistencias_hoy)
                print("Salidas encontradas:", salidas_hoy)

        except Exception as e:
            print(f"Error en la consulta: {str(e)}")
            flash("Error al consultar la base de datos.", "danger")
        finally:
            conn.close()

        if descargar_pdf:
            return generar_pdf(asistencias_hoy)

    return render_template('administracion.html', 
                           asistencias_hoy=asistencias_hoy, 
                           salidas_hoy=salidas_hoy,
                           busqueda=busqueda,
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin)

if __name__ == '__main__':
    app.run(debug=True)
