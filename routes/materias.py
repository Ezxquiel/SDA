from flask import Blueprint, render_template, request
from models.datos import get_db_connection

asistencias_class_bp = Blueprint('asistencias_class', __name__)

@asistencias_class_bp.route('/asistencia_por_materia', methods=['GET', 'POST'])
def asistencia_por_materia():
    selected_materia = request.form.get('materia')  # Materia seleccionada en el formulario

    # Conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener las materias para el select
    cursor.execute("SELECT id_materia, materia FROM materias")
    materias = cursor.fetchall()

    if selected_materia:
        # Obtener las asistencias de la materia seleccionada
        cursor.execute("""
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
                s.año,  -- Año de la sección
                s.seccion -- Sección del estudiante
            FROM
                asistencia_materia am
            JOIN
                estudiantes e ON am.id_estudiante = e.id_estudiante
            JOIN
                materias m ON am.materia = m.id_materia
            LEFT JOIN
                justificaciones j ON am.id_justificacion = j.id_justificacion
            JOIN
                seccion s ON e.año = s.año AND e.seccion = s.seccion  -- Unir con la tabla de secciones
            WHERE
                am.materia = %s
        """, (selected_materia,))
        asistencias = cursor.fetchall()
    else:
        # Obtener todas las asistencias si no se seleccionó una materia
        cursor.execute("""
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
                s.año,  -- Año de la sección
                s.seccion -- Sección del estudiante
            FROM
                asistencia_materia am
            JOIN
                estudiantes e ON am.id_estudiante = e.id_estudiante
            JOIN
                materias m ON am.materia = m.id_materia
            LEFT JOIN
                justificaciones j ON am.id_justificacion = j.id_justificacion
            JOIN
                seccion s ON e.año = s.año AND e.seccion = s.seccion  -- Unir con la tabla de secciones
        """)
        asistencias = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'asistencia_por_materia.html',
        materias=materias,
        asistencias=asistencias,
        selected_materia=selected_materia
    )
