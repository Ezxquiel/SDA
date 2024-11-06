from flask import Blueprint, request, flash, redirect, url_for, render_template
from models.database import db_operation, get_db_connection
from datetime import datetime, date


admin_mañana_bp = Blueprint('admin_mañana', __name__)

@admin_mañana_bp.route('/administracionAM', methods=['GET', 'POST'])
def administracionM():

    try:
        conn = get_db_connection()
        if not conn:
            flash("No se pudo conectar a la base de datos.", "danger")
            return render_template('matutino.html', resumen=[], totales={}, busqueda='', fecha_inicio='', fecha_fin='')

        resumen = []
        totales = {}
        busqueda = ''
        fecha_inicio = date.today()
        fecha_fin = date.today()

        if request.method == 'POST':
            busqueda = request.form.get('busqueda', '').strip()
            fecha_inicio = request.form.get('fecha_inicio', str(fecha_inicio))
            fecha_fin = request.form.get('fecha_fin', str(fecha_fin))
            mostrar_todo = request.form.get('mostrar_todo')

            # Si se presiona el botón de mostrar todo, ignoramos la búsqueda
            if mostrar_todo:
                busqueda = ''

            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

                if fecha_fin < fecha_inicio:
                    flash("La fecha final no puede ser menor que la fecha inicial.", "warning")
                    fecha_fin = fecha_inicio

            except ValueError:
                flash("Formato de fecha inválido. Usando fecha actual.", "warning")
                fecha_inicio = date.today()
                fecha_fin = date.today()

            try:
                with conn.cursor() as cursor:
                    # Consulta principal con filtro de búsqueda
                    consulta_detalle = """
                        SELECT
                            sec.año,
                            sec.seccion,
                            COUNT(DISTINCT e.nie) AS total_asistidos,
                            COUNT(DISTINCT CASE WHEN est.genero = 'M' AND e.nie IS NOT NULL THEN e.nie END) AS total_masculino,
                            COUNT(DISTINCT CASE WHEN est.genero = 'F' AND e.nie IS NOT NULL THEN e.nie END) AS total_femenino,
                            COUNT(CASE WHEN e.nie IS NULL THEN 1 END) AS total_inasistidos,
                            ROUND(100.0 * COUNT(DISTINCT e.nie) / NULLIF(COUNT(DISTINCT e.nie) + COUNT(CASE WHEN e.nie IS NULL THEN 1 END), 0), 2) AS porcentaje_asistencia,
                            GROUP_CONCAT(CASE WHEN e.nie IS NULL THEN est.codigo END) AS codigos_inasistidos,
                            GROUP_CONCAT(CASE WHEN e.nie IS NOT NULL THEN est.codigo END) AS codigos_asistidos
                        FROM estudiantes est
                        LEFT JOIN entrada e ON est.nie = e.nie AND DATE(e.fecha) BETWEEN %s AND %s
                        JOIN seccion sec ON est.año = sec.año AND est.seccion = sec.seccion
                        WHERE est.genero IN ('M', 'F')
                        AND (e.nie IS NULL OR TIME(e.hora) BETWEEN '04:00:00' AND '12:44:59')
                        {0}
                        GROUP BY sec.año, sec.seccion
                        ORDER BY sec.año, sec.seccion
                    """.format("AND CONCAT(sec.año, sec.seccion) LIKE %s" if busqueda else "")

                    # Consulta para totales
                    consulta_totales = """
                        SELECT
                            COUNT(DISTINCT e.nie) AS total_asistidos,
                            COUNT(DISTINCT CASE WHEN est.genero = 'M' AND e.nie IS NOT NULL THEN e.nie END) AS total_masculino,
                            COUNT(DISTINCT CASE WHEN est.genero = 'F' AND e.nie IS NOT NULL THEN e.nie END) AS total_femenino,
                            COUNT(CASE WHEN e.nie IS NULL THEN 1 END) AS total_inasistidos,
                            ROUND(100.0 * COUNT(DISTINCT e.nie) / NULLIF(COUNT(DISTINCT e.nie) + COUNT(CASE WHEN e.nie IS NULL THEN 1 END), 0), 2) AS porcentaje_asistencia
                        FROM estudiantes est
                        LEFT JOIN entrada e ON est.nie = e.nie AND DATE(e.fecha) BETWEEN %s AND %s
                        JOIN seccion sec ON est.año = sec.año AND est.seccion = sec.seccion
                        WHERE est.genero IN ('M', 'F')
                        AND (e.nie IS NULL OR TIME(e.hora) BETWEEN '04:00:00' AND '12:44:59')
                        {0}
                    """.format("AND CONCAT(sec.año, sec.seccion) LIKE %s" if busqueda else "")

                    # Preparar parámetros según si hay búsqueda o no
                    params_detalle = [fecha_inicio, fecha_fin]
                    params_totales = [fecha_inicio, fecha_fin]
                    
                    if busqueda:
                        busqueda_patron = f'%{busqueda}%'
                        params_detalle.append(busqueda_patron)
                        params_totales.append(busqueda_patron)
                    
                    # Ejecutar consultas
                    cursor.execute(consulta_detalle, tuple(params_detalle))
                    resumen = cursor.fetchall()

                    cursor.execute(consulta_totales, tuple(params_totales))
                    totales = cursor.fetchone()

            except Exception as e:
                print(f"Error en la consulta: {str(e)}")
                flash("Error al consultar la base de datos.", "danger")
                return render_template('matutino.html', resumen=[], totales={}, busqueda=busqueda, 
                                    fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

    except Exception as e:
        print(f"Error general: {str(e)}")
        flash("Ocurrió un error inesperado.", "danger")
        return render_template('matutino.html', resumen=[], totales={}, busqueda='', 
                             fecha_inicio='', fecha_fin='')

    finally:
        if conn:
            conn.close()


    return render_template('matutino.html', resumen=resumen, totales=totales, busqueda=busqueda, 
                         fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)