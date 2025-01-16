from flask import Blueprint, request, flash, redirect, url_for, render_template
from models.database import db_operation
from datetime import datetime
import pymysql

aulapm_bp = Blueprint('aulapm', __name__)

@aulapm_bp.route('/gestionar_aulapm', methods=['GET', 'POST'])
@db_operation
def gestionar_aula(cursor):
    # Inicializar variables para la plantilla
    estudiantes = []
    año_selected = None
    seccion_selected = None

    # Obtener los valores de años y secciones para los dropdowns
    cursor.execute("SELECT DISTINCT año FROM estudiantes")
    años = cursor.fetchall()
    cursor.execute("SELECT DISTINCT seccion FROM estudiantes")
    secciones = cursor.fetchall()

    if request.method == 'POST':
        if 'buscar' in request.form:
            # Obtener datos del formulario
            año = request.form.get('año')
            seccion = request.form.get('seccion')
            fecha_actual = datetime.now().date()  # Fecha actual

            try:
                # Consulta para obtener estudiantes con entrada registrada hoy
                query = """
                    SELECT e.id_estudiante, e.nombre, e.codigo
                    FROM estu
                    INNER JOIN entradadiantes e en ON e.id_estudiante = en.nie
                    WHERE e.año = %s 
                      AND e.seccion = %s
                      AND DATE(en.fecha_entrada) = %s
                      AND TIME(en.hora_entrada) BETWEEN '12:00:00' AND '19:00:00'
                """
                cursor.execute(query, (año, seccion, fecha_actual))
                estudiantes = cursor.fetchall()

                if not estudiantes:
                    flash('No se encontraron estudiantes con entrada registrada hoy.', 'warning')
                else:
                    flash(f'Se encontraron {len(estudiantes)} estudiantes.', 'success')

                return render_template('aula_pm.html',
                                       años=años,
                                       secciones=secciones,
                                       estudiantes=estudiantes,
                                       año=año,
                                       seccion=seccion)

            except pymysql.Error as e:
                flash(f'Error al buscar estudiantes: {str(e)}', 'danger')
                return render_template('aula_pm.html',
                                       años=años,
                                       secciones=secciones,
                                       estudiantes=estudiantes)

        elif 'registrar' in request.form:
            try:
                # Procesar el registro de asistencia
                id_estudiantes = request.form.getlist('id_estudiante[]')
                estados = request.form.getlist('estado[]')
                materia = request.form.get('materia')
                maestro = request.form.get('maestro')
                fecha_clase = datetime.now().date()
                hora_clase = datetime.now().time()

                for id_estudiante, estado in zip(id_estudiantes, estados):
                    query = """
                        INSERT INTO asistencia_materia 
                        (id_estudiante, materia, fecha_clase, hora_clase, estado, maestro)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (id_estudiante, materia, fecha_clase, hora_clase, estado, maestro))

                flash('Asistencia registrada exitosamente.', 'success')
                return redirect(url_for('aulapm.gestionar_aula'))

            except pymysql.Error as e:
                flash(f'Error al registrar asistencia: {str(e)}', 'danger')
                return redirect(url_for('aulapm.gestionar_aula'))

    # Respuesta por defecto para solicitudes GET
    return render_template('aula_pm.html',
                           años=años,
                           secciones=secciones,
                           estudiantes=estudiantes,
                           año=año_selected,
                           seccion=seccion_selected)
