from flask import Blueprint, request, flash, redirect, url_for, render_template
from models.database import db_operation
from datetime import datetime
import pymysql

aula_bp = Blueprint('aula', __name__)

@aula_bp.route('/gestionar_aula', methods=['GET', 'POST'])
@db_operation
def gestionar_aula(cursor):
    if request.method == 'POST':
        if 'buscar' in request.form:
            # Obtener año y sección del formulario
            año = request.form.get('año')
            seccion = request.form.get('seccion')

            # Imprimir los valores para verificar si están llegando correctamente
            print(f"Año seleccionado: {año}")
            print(f"Sección seleccionada: {seccion}")

            # Consulta para obtener los estudiantes del año y la sección seleccionados
            query = """
                SELECT id_estudiante, nombre, codigo
                FROM estudiantes 
                WHERE año = %s AND seccion = %s
            """
            cursor.execute(query, (año, seccion))
            estudiantes = cursor.fetchall()

            if not estudiantes:
                flash('No se encontraron estudiantes para la selección realizada', 'warning')
                return redirect(url_for('aula.gestionar_aula'))

            # Renderizar la lista de estudiantes encontrados
            return render_template('aula.html', estudiantes=estudiantes, año=año, seccion=seccion)

        elif 'registrar' in request.form:
            # Obtener los datos del formulario
            id_estudiantes = request.form.getlist('id_estudiante[]')
            estados = request.form.getlist('estado[]')
            materia = request.form.get('materia')
            maestro = request.form.get('maestro')
            fecha_clase = datetime.now().date()  # Fecha actual por defecto
            hora_clase = datetime.now().time()   # Hora actual por defecto

            # Verificar que los datos se estén recibiendo correctamente
            print(f"ID Estudiantes: {id_estudiantes}")
            print(f"Estados: {estados}")
            print(f"Materia: {materia}")
            print(f"Maestro: {maestro}")

            try:
                # Insertar la asistencia de todos los estudiantes
                for id_estudiante, estado in zip(id_estudiantes, estados):
                    query = """
                        INSERT INTO asistencia_materia 
                        (id_estudiante, materia, fecha_clase, hora_clase, estado, maestro)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (id_estudiante, materia, fecha_clase, hora_clase, estado, maestro))
                
                flash('Asistencia registrada exitosamente para todos los estudiantes', 'success')
                return redirect(url_for('aula.gestionar_aula'))

            except pymysql.Error as e:
                print(f"Error SQL: {str(e)}")  # Imprimir el error completo para mayor claridad
                flash(f'Error al registrar asistencia: {str(e)}', 'danger')
                return redirect(url_for('aula.gestionar_aula'))

    # Si es GET, mostrar formulario para seleccionar año y sección
    cursor.execute("SELECT DISTINCT año FROM estudiantes")
    años = cursor.fetchall()

    cursor.execute("SELECT DISTINCT seccion FROM estudiantes")
    secciones = cursor.fetchall()

    return render_template('aula.html', años=años, secciones=secciones)
