from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from models.database import db_operation
from utils.auth_utils import login_required

students_bp = Blueprint('students', __name__)

@students_bp.route('/estudiantes', methods=['GET', 'POST'])
@db_operation
def estudiantes_router(cursor):
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder", "warning")
        return redirect('/login')
    # Fetch form data


    cursor.execute("SELECT seccion FROM seccion")
    secciones = [row['seccion'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT año FROM seccion")
    anios = [row['año'] for row in cursor.fetchall()]

    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            nie = request.form['nie']
            edad = request.form['edad']
            año = request.form['año']
            codigo = request.form['codigo']

            seccion = request.form['seccion']
            genero = request.form['genero']

            
            # Verify section exists
            cursor.execute("SELECT * FROM seccion WHERE seccion = %s AND año = %s", 
                         (seccion, año))
            seccion_exists = cursor.fetchone()
            if not seccion_exists:
                flash('La sección o año especificado no existe.', 'danger')
                return redirect(url_for('students.estudiantes_router'))

            # Insert student
            cursor.execute("""
                INSERT INTO estudiantes 
                (nombre, nie, edad, año, codigo, seccion, genero) 
                VALUES (%s, %s, %s, %s, %s, %s,  %s)
            """, (nombre, nie, edad, año, codigo, seccion, genero))
            
            flash('Alumno registrado con éxito.', 'success')
            
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:
                flash('Error: El NIE ya está registrado.', 'danger')
            else:
                flash(f'Error en la base de datos: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
            
        return redirect(url_for('students.estudiantes_router'))

    return render_template('estudiantes.html',  secciones=secciones, anios=anios, web_name='Estudiantes')