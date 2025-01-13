from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from models.database import get_db_connection
from utils.auth_utils import login_required, admin_required
from pymysql.cursors import DictCursor
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

informeAM_bp = Blueprint('informeAM', __name__)

class DatabaseManager:
    def __init__(self):
        self.conexion = None
        self.cursor = None

    def __enter__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor(DictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
        if exc_type:
            logger.error(f"Error en la base de datos: {str(exc_val)}")
            return False

class EstudiantesQueries:
    @staticmethod
    def get_asistidos_query() -> str:
        return """
        SELECT 
            e.nie,
            e.nombre,
            e.codigo,
            MAX(ent.fecha_entrada) AS fecha_entrada,
            MAX(ent.hora_entrada) AS hora_entrada
        FROM estudiantes e
        LEFT JOIN entrada ent ON e.nie = ent.nie
        WHERE e.año = %s 
        AND e.seccion = %s
        AND DATE(ent.fecha_entrada) BETWEEN %s AND %s
        AND ent.hora_entrada BETWEEN '04:00:00' AND '12:58:00'
        GROUP BY e.nie, e.nombre, e.codigo
        """

    @staticmethod
    def get_inasistidos_query() -> str:
        return """
        SELECT 
            e.nie,
            e.nombre,
            e.codigo
        FROM estudiantes e
        LEFT JOIN entrada ent ON e.nie = ent.nie
            AND DATE(ent.fecha_entrada) BETWEEN %s AND %s
            AND ent.hora_entrada BETWEEN '04:00:00' AND '12:58:00'
        WHERE e.año = %s 
        AND e.seccion = %s
        AND ent.nie IS NULL
        """

class DateRangeValidator:
    @staticmethod
    def validate(fecha_inicio_str: Optional[str] = None, fecha_fin_str: Optional[str] = None) -> Tuple[date, date]:
        today = date.today()
        try:
            if fecha_inicio_str:
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            else:
                fecha_inicio = today

            if fecha_fin_str:
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            else:
                fecha_fin = today

            if fecha_fin < fecha_inicio:
                fecha_fin = fecha_inicio

            return fecha_inicio, fecha_fin

        except ValueError as e:
            logger.warning(f"Error en formato de fecha: {str(e)}")
            return today, today

class EstudiantesService:
    @staticmethod
    def obtener_estudiantes_asistidos(anio: int, seccion: str, fecha_inicio: date, fecha_fin: date) -> List[Dict]:
        try:
            with DatabaseManager() as db:
                db.cursor.execute(
                    EstudiantesQueries.get_asistidos_query(),
                    (anio, seccion, fecha_inicio, fecha_fin)
                )
                return db.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error al obtener estudiantes asistidos: {str(e)}")
            return []

    @staticmethod
    def obtener_estudiantes_inasistidos(anio: int, seccion: str, fecha_inicio: date, fecha_fin: date) -> List[Dict]:
        try:
            with DatabaseManager() as db:
                db.cursor.execute(
                    EstudiantesQueries.get_inasistidos_query(),
                    (fecha_inicio, fecha_fin, anio, seccion)
                )
                return db.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error al obtener estudiantes inasistidos: {str(e)}")
            return []

@informeAM_bp.route('/detalles_seccion/<int:anio>/<seccion>')
@login_required
@admin_required
def ruta_detalles_seccion(anio: int, seccion: str):
    try:
        # Obtener fechas de los query params o session
        fecha_inicio_str = request.args.get('fecha_inicio') or session.get('fecha_inicio')
        fecha_fin_str = request.args.get('fecha_fin') or session.get('fecha_fin')
        
        # Validar fechas
        fecha_inicio, fecha_fin = DateRangeValidator.validate(fecha_inicio_str, fecha_fin_str)
        
        # Guardar fechas en sesión
        session['fecha_inicio'] = fecha_inicio.strftime('%Y-%m-%d')
        session['fecha_fin'] = fecha_fin.strftime('%Y-%m-%d')

        # Obtener datos de asistidos e inasistidos
        asistidos = EstudiantesService.obtener_estudiantes_asistidos(anio, seccion, fecha_inicio, fecha_fin)
        inasistidos = EstudiantesService.obtener_estudiantes_inasistidos(anio, seccion, fecha_inicio, fecha_fin)

        # Validar si hay datos
        if not asistidos and not inasistidos:
            flash(f"No hay datos disponibles para la sección {seccion} del año {anio} en el rango de fechas seleccionado.", "info")
            return redirect(url_for('informeAM.home'))

        # Preparar estadísticas
        estadisticas = {
            'total_estudiantes': len(asistidos) + len(inasistidos),
            'total_asistidos': len(asistidos),
            'total_inasistidos': len(inasistidos),
            'porcentaje_asistencia': round(len(asistidos) * 100 / (len(asistidos) + len(inasistidos)), 2) if (len(asistidos) + len(inasistidos)) > 0 else 0,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        }

        return render_template(
            'detalles_seccion.html',
            anio=anio,
            seccion=seccion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            alumnos_con_asistencia=asistidos,
            alumnos_sin_asistencia=inasistidos,
            estadisticas=estadisticas
        )

    except Exception as e:
        logger.error(f"Error en ruta_detalles_seccion: {str(e)}")
        flash("Ocurrió un error al procesar la solicitud.", "danger")
        return redirect(url_for('informeAM.home'))