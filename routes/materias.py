from flask import Blueprint, render_template
from models.datos import get_db_connection

asistencias_class_bp = Blueprint('asistencias_class', __name__)

@asistencias_class_bp.route('/asistencia_por_materia', methods=['GET'])
def asistencia_por_materia():
    materias = []  # Variable para almacenar las materias disponibles

    # Conexión a la base de datos para obtener las materias
    conn = get_db_connection()
    cursor = conn.cursor()  # Sin el argumento dictionary=True
    cursor.execute("SELECT id_materia, materia FROM materias")
    materias = cursor.fetchall()  # Recuperamos todas las materias
    cursor.close()
    conn.close()

    # Retornar la plantilla con las materias
    return render_template('asistencia_por_materia.html', materias=materias)
