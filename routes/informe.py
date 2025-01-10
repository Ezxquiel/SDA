from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from models.database import db_operation, get_db_connection
from datetime import datetime, date
from utils.auth_utils import login_required, admin_required
import pymysql
from pymysql.cursors import DictCursor  

informe_bp = Blueprint('informe', __name__)

# Función para obtener datos detallados de los estudiantes (con asistencia)
def obtener_datos_detallados(anio, seccion):
    conexion = get_db_connection()  # Función de conexión a la base de datos
    cursor = conexion.cursor(DictCursor)  # Usa el cursor de tipo diccionario

    query = """
    SELECT 
        e.nie, e.nombre, e.codigo, MAX(ent.fecha_entrada) AS fecha_entrada, MAX(ent.hora_entrada) AS hora_entrada
    FROM estudiantes e
    LEFT JOIN entrada ent ON e.nie = ent.nie
    WHERE e.año = %s AND e.seccion = %s
    GROUP BY e.nie, e.nombre, e.codigo
    """
    cursor.execute(query, (anio, seccion))
    alumnos = cursor.fetchall()  # Obtiene todos los resultados como diccionarios

    cursor.close()
    conexion.close()
    return alumnos

# Función para obtener estudiantes sin asistencia (sin entradas registradas hoy)
def obtener_estudiantes_sin_asistencia(anio, seccion):
    conexion = get_db_connection()
    cursor = conexion.cursor(DictCursor)  
    query = """
    SELECT 
        e.nie, e.nombre
    FROM estudiantes e
    LEFT JOIN entrada ent ON e.nie = ent.nie AND ent.fecha_entrada = CURDATE()
    WHERE e.año = %s AND e.seccion = %s
      AND ent.nie IS NULL
    """
    cursor.execute(query, (anio, seccion))
    estudiantes_sin_asistencia = cursor.fetchall()  # Obtiene todos los resultados como diccionarios

    cursor.close()
    conexion.close()
    return estudiantes_sin_asistencia

# Ruta para ver los detalles de los estudiantes por año y sección
@informe_bp.route('/detalles_seccion/<anio>/<seccion>')
@login_required  
@admin_required  
def ruta_detalles_seccion(anio, seccion):
    # Validar el formato del año
    try:
        anio = int(anio)  # Convierte el parámetro anio a entero
    except ValueError:
        flash("El año ingresado no es válido.", "error")
        return redirect(url_for('home'))  # Redirige al inicio si el año no es válido

    # Obtener los datos de los alumnos para ese año y sección
    datos_alumnos = obtener_datos_detallados(anio, seccion)

    # Obtener los estudiantes sin asistencia para ese año y sección
    estudiantes_sin_asistencia = obtener_estudiantes_sin_asistencia(anio, seccion)

    # Manejar casos sin datos
    if not datos_alumnos and not estudiantes_sin_asistencia:
        flash(f"No hay datos disponibles para la sección {seccion} del año {anio}.", "info")
        return redirect(url_for('informe.home'))  # Redirige si no hay datos

    # Renderiza la plantilla con los datos obtenidos
    return render_template('detalles_seccion.html', anio=anio, seccion=seccion, 
                           alumnos_con_asistencia=datos_alumnos, 
                           estudiantes_sin_asistencia=estudiantes_sin_asistencia)
