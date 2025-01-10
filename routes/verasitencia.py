from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from utils.auth_utils import login_required
from flask import Flask, render_template, request, flash
from config.config import Config
from models.datos import get_db_connection
import logging
import datetime

verasitencia_bp = Blueprint('verasitencia_bp', __name__)

@verasitencia_bp.route('/verasistencia', methods=['GET', 'POST'])
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
                        """SELECT e.*, ent.id_entrada, ent.fecha, ent.hora 
                           FROM entrada ent
                           JOIN estudiantes e ON ent.nie = e.nie 
                           WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                           ORDER BY ent.fecha DESC, ent.hora DESC""",
                        ('%' + busqueda + '%', '%' + busqueda + '%')
                    )
                    asistencias_hoy2 = cursor.fetchall()
                    logging.info(f"Resultados de asistencias: {asistencias_hoy2}")

                    # Consulta para salidas
                    cursor.execute(
                        """SELECT e.nombre, e.codigo, e.nie, sal.id_salida, sal.fecha, sal.hora 
                           FROM salida sal
                           JOIN estudiantes e ON sal.nie = e.nie 
                           WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                           ORDER BY sal.fecha DESC, sal.hora DESC""",
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

    return render_template('verasitencia_bp.html', asistencias_hoy=asistencias_hoy2, salidas_hoy=salidas_hoy, busqueda=busqueda, web_name=titulo_web)
