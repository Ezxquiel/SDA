from flask import Blueprint, render_template, request
from datetime import datetime
from models.datos import get_db_connection

asistencias_class_bp = Blueprint('asistencias_class', __name__)

@asistencias_class_bp.route('/asistencia_por_materia', methods=['GET', 'POST'])
def asistencia_por_materia():
    selected_materia = request.form.get('materia')  # Materia seleccionada
    selected_año = request.form.get('año')          # Año seleccionado
    selected_seccion = request.form.get('seccion')  # Sección seleccionada
    selected_fecha = request.form.get('fecha')      # Fecha seleccionada

    # Si no se ha seleccionado una fecha, usar la fecha de hoy
    if not selected_fecha:
        selected_fecha = datetime.today().strftime('%Y-%m-%d')

    # Conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener las materias para el select
    cursor.execute("SELECT id_materia, materia FROM materias")
    materias = cursor.fetchall()

    # Obtener los años y secciones para los filtros
    cursor.execute("SELECT DISTINCT año FROM seccion")
    años = cursor.fetchall()

    cursor.execute("SELECT DISTINCT seccion FROM seccion")
    secciones = cursor.fetchall()

    # Construir la consulta dinámica
    query = """
        SELECT
            am.id_asistencia_materia,
            am.id_estudiante,
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

    cursor.close()
    conn.close()

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
