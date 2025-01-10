from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from models.database import db_operation
from utils.auth_utils import login_required
from models.database import get_db_connection
from flask import Flask, render_template, request, flash
from config.config import Config
from models.database import db_operation, get_db_connection
import logging
import datetime

sections_bp = Blueprint('sections_bp', __name__)

@sections_bp.route('/verasistencia', methods=['GET', 'POST'])
def index():
    titulo_web = "Inicio"
    conn = get_db_connection()

    if not conn:
        flash("No se pudo conectar a la base de datos.", "danger")
        return render_template('index.html', asistencias_hoy=[], salidas_hoy=[], busqueda='')

    asistencias_hoy2 = []
    salidas_hoy = []
    busqueda = ''

    if request.method == 'POST':
        busqueda = request.form.get('busqueda', '').strip()
        logging.info(f"[{datetime.datetime.now()}] Buscando por: {busqueda}")
        
        if busqueda:
            try:
                with conn.cursor() as cursor:
                    # Consulta para entradas
                    cursor.execute(
                        """SELECT e.*, ent.id_entrada, ent.fecha_entrada, ent.hora_entrada
                           FROM entrada ent
                           JOIN estudiantes e ON ent.nie = e.nie 
                           WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                           ORDER BY ent.fecha_entrada DESC, ent.hora_entrada DESC""",
                        ('%' + busqueda + '%', '%' + busqueda + '%')
                    )
                    asistencias_hoy2 = cursor.fetchall()
                    logging.info(f"Resultados de asistencias: {asistencias_hoy2}")

                    # Consulta para salidas
                    cursor.execute(
                        """SELECT e.nombre, e.codigo, e.nie, sal.id_salida, sal.fecha_salida, sal.hora_salida 
                           FROM salida sal
                           JOIN estudiantes e ON sal.nie = e.nie 
                           WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                           ORDER BY sal.fecha_salida DESC, sal.hora_salida DESC""",
                        ('%' + busqueda + '%', '%' + busqueda + '%')
                    )
                    salidas_hoy = cursor.fetchall()
                    logging.info(f"Resultados de salidas: {salidas_hoy}")

                    # Mensaje si no hay resultados
                    if not asistencias_hoy2 and not salidas_hoy:
                        flash("No se encontraron registros para la búsqueda.", "info")

            except Exception as e:
                logging.error(f"Error en la consulta: {str(e)}")
                flash("Error al consultar la base de datos.", "danger")
            finally:
                conn.close()  
        else:
            flash("Por favor, ingresa un NIE o Código para buscar.", "warning")

    return render_template('verAsistencia.html', asistencias_hoy=asistencias_hoy2, salidas_hoy=salidas_hoy, busqueda=busqueda, titulo_web=titulo_web)
