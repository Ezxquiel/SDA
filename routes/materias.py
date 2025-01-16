from flask import Flask, Blueprint, render_template, request
from datetime import datetime
from models.datos import get_db_connection

# Blueprint para manejo de asistencias
asistencias_class_bp = Blueprint('asistencias_class', __name__)

@asistencias_class_bp.route('/asistencia_por_materia', methods=['GET', 'POST'])
def asistencia_por_materia():
    # Obtener los datos del formulario
    selected_materia = request.form.get('materia')
    selected_año = request.form.get('año')
    selected_seccion = request.form.get('seccion')
    selected_fecha = request.form.get('fecha')

    # Si no se selecciona fecha, usar la fecha actual
    if not selected_fecha:
        selected_fecha = datetime.today().strftime('%Y-%m-%d')

    # Conexión a la base de datos
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Obtener materias, años y secciones para los filtros
            cursor.execute("SELECT id_materia, materia FROM materias")
            materias = cursor.fetchall()

            cursor.execute("SELECT DISTINCT año FROM seccion")
            años = cursor.fetchall()

            cursor.execute("SELECT DISTINCT seccion FROM seccion")
            secciones = cursor.fetchall()

            # Consulta para obtener asistencias
            query = """
                SELECT
                    am.id_asistencia_materia,
                    e.nombre AS estudiante,
                    m.materia,
                    am.fecha_clase,
                    am.hora_clase,
                    am.maestro,
                    am.estado,
                    j.tipo AS justificacion,
                    s.año,
                    s.seccion
                FROM
                    asistencia_materia am
                JOIN
                    estudiantes e ON am.id_estudiante = e.id_estudiante
                JOIN
                    materias m ON am.materia = m.id_materia
                LEFT JOIN
                    justificaciones j ON am.id_justificacion = j.id_justificacion
                JOIN
                    seccion s ON e.año = s.año AND e.seccion = s.seccion
                WHERE am.fecha_clase = %s
            """
            params = [selected_fecha]

            if selected_materia:
                query += " AND am.materia = %s"
                params.append(selected_materia)

            if selected_año:
                query += " AND s.año = %s"
                params.append(selected_año)

            if selected_seccion:
                query += " AND s.seccion = %s"
                params.append(selected_seccion)

            cursor.execute(query, params)
            asistencias = cursor.fetchall()

    # Renderizar el template con los datos
    return render_template(
        'asistencia_por_materia.html',
        materias=materias,
        años=años,
        secciones=secciones,
        asistencias=asistencias,
        selected_materia=selected_materia,
        selected_año=selected_año,
        selected_seccion=selected_seccion,
        selected_fecha=selected_fecha
    )

