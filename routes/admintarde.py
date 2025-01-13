
# routes.py
import pymysql 
from flask import Blueprint, request, flash, redirect, url_for, render_template, send_file, session
from models.database import db_operation, get_db_connection
from datetime import datetime, date
from utils.pdf_generator import AttendanceReport
from utils.auth_utils import login_required, admin_required



admintarde_bp = Blueprint('admintarde', __name__)

@admintarde_bp.route('/admintardePM', methods=['GET', 'POST'])
def administracionPM():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder", "warning")
        return redirect('/login')
        
    try:
        conn = get_db_connection()
        if not conn:
            flash("No se pudo conectar a la base de datos.", "danger")
            return render_template('vespertino.html', resumen=[], totales={}, busqueda='', fecha_inicio='', fecha_fin='')

        resumen = []
        totales = {}
        busqueda = ''
        fecha_inicio = date.today()
        fecha_fin = date.today()

        if request.method == 'POST':
            busqueda = request.form.get('busqueda', '').strip()
            fecha_inicio_str = request.form.get('fecha_inicio', str(fecha_inicio))
            fecha_fin_str = request.form.get('fecha_fin', str(fecha_fin))
            mostrar_todo = request.form.get('mostrar_todo')
            descargar_pdf = request.form.get('descargar_pdf')

            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()

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
                            GROUP_CONCAT(CASE WHEN e.nie IS NULL THEN est.nombre END) AS codigos_inasistidos,
                            GROUP_CONCAT(CASE WHEN e.nie IS NOT NULL THEN est.nombre END) AS codigos_asistidos,
                            MIN(DATE(e.fecha_entrada)) AS fecha_primera_asistencia,
                            DATE(e.fecha_entrada) AS fecha_entrada
                        FROM estudiantes est
                        LEFT JOIN entrada e ON est.nie = e.nie AND DATE(e.fecha_entrada) BETWEEN %s AND %s
                        JOIN seccion sec ON est.año = sec.año AND est.seccion = sec.seccion
                        WHERE est.genero IN ('M', 'F')
                        AND (e.nie IS NULL OR TIME(e.hora_entrada) BETWEEN '12:45:00' AND '21:00:00')
                        {0}
                        GROUP BY sec.año, sec.seccion, DATE(e.fecha_entrada)
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
                        LEFT JOIN entrada e ON est.nie = e.nie AND DATE(e.fecha_entrada) BETWEEN %s AND %s
                        JOIN seccion sec ON est.año = sec.año AND est.seccion = sec.seccion
                        WHERE est.genero IN ('M', 'F')
                        AND (e.nie IS NULL OR TIME(e.hora_entrada) BETWEEN '12:45:00' AND '21:00:00')
                        {0}
                    """.format("AND CONCAT(sec.año, sec.seccion) LIKE %s" if busqueda else "")

                    # Preparar parámetros
                    params_detalle = [fecha_inicio, fecha_fin]
                    params_totales = [fecha_inicio, fecha_fin]
                    
                    if busqueda:
                        params_detalle.append(f'%{busqueda}%')
                        params_totales.append(f'%{busqueda}%')

                    # Ejecutar consultas
                    cursor.execute(consulta_detalle, tuple(params_detalle))
                    resumen = cursor.fetchall()
                    
                    cursor.execute(consulta_totales, tuple(params_totales))
                    totales = cursor.fetchone()

                    # Verificar si se debe generar PDF
                    if descargar_pdf and resumen and totales:
                        try:
                            report = AttendanceReport(resumen, totales, fecha_inicio, fecha_fin)
                            pdf_filename = report.generate()
                            
                            return send_file(
                                pdf_filename,
                                mimetype='application/pdf',
                                as_attachment=True,
                                download_name='reporte_asistencia.pdf'
                            )
                        except Exception as e:
                            print(f"Error al generar PDF: {str(e)}")
                            flash("Error al generar el PDF.", "danger")

            except Exception as e:
                print(f"Error en la consulta: {str(e)}")
                flash("Error al consultar la base de datos.", "danger")

    except Exception as e:
        print(f"Error general: {str(e)}")
        flash("Ocurrió un error inesperado.", "danger")
        return render_template('vespertino.html', resumen=[], totales={}, busqueda='', 
                             fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

    finally:
        if conn:
            conn.close()

    # Add the date and day of the week to each record in the summary
    for record in resumen:
        record['fecha'] = record['fecha_entrada'].strftime('%Y-%m-%d') if record['fecha_entrada'] else fecha_inicio.strftime('%Y-%m-%d')
        record['dia_semana'] = record['fecha_entrada'].strftime('%A') if record['fecha_entrada'] else fecha_inicio.strftime('%A')

    return render_template('vespertino.html', resumen=resumen, totales=totales, busqueda=busqueda, 
                         fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, web_name='Vespertino')


@admintarde_bp.route('/detalles/seccion', methods=['GET'])
def buscar_detalles_asistencia():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder", "warning")
        return redirect('/login')

    anio = request.args.get('anio', '').strip()
    seccion = request.args.get('seccion', '').strip()

    # Validación de los parámetros recibidos
    if not anio or not seccion:
        flash("Por favor ingresa un año y una sección válidos.", "warning")
        return redirect(url_for('admintarde.buscar_detalles_asistencia'))

    try:
        conn = get_db_connection()
        if not conn:
            flash("No se pudo conectar a la base de datos.", "danger")
            return render_template('detalles.html', resumen=[], totales={}, anio=anio, seccion=seccion)

        resumen = []
        totales = {}

        # Consulta de detalles de asistencia
        consulta_detalle = """
            SELECT
                sec.año,
                sec.seccion,
                COUNT(DISTINCT e.nie) AS total_asistidos,
                COUNT(DISTINCT CASE WHEN est.genero = 'M' AND e.nie IS NOT NULL THEN e.nie END) AS total_masculino,
                COUNT(DISTINCT CASE WHEN est.genero = 'F' AND e.nie IS NOT NULL THEN e.nie END) AS total_femenino,
                COUNT(CASE WHEN e.nie IS NULL THEN 1 END) AS total_inasistidos,
                ROUND(100.0 * COUNT(DISTINCT e.nie) / NULLIF(COUNT(DISTINCT e.nie) + COUNT(CASE WHEN e.nie IS NULL THEN 1 END), 0), 2) AS porcentaje_asistencia,
                GROUP_CONCAT(CASE WHEN e.nie IS NULL THEN est.nombre END) AS codigos_inasistidos,
                GROUP_CONCAT(CASE WHEN e.nie IS NOT NULL THEN est.nombre END) AS codigos_asistidos,
                MIN(DATE(e.fecha_entrada)) AS fecha_primera_asistencia,
                DATE(e.fecha_entrada) AS fecha_entrada
            FROM estudiantes est
            LEFT JOIN entrada e ON est.nie = e.nie
            JOIN seccion sec ON est.año = sec.año AND est.seccion = sec.seccion
            WHERE est.genero IN ('M', 'F')
            AND CONCAT(sec.año, sec.seccion) LIKE %s
            GROUP BY sec.año, sec.seccion, DATE(e.fecha_entrada)
            ORDER BY sec.año, sec.seccion
        """

        params_detalle = [f'{anio}{seccion}']

        with conn.cursor() as cursor:
            cursor.execute(consulta_detalle, tuple(params_detalle))
            resumen = cursor.fetchall()

            # Obtener los totales
            consulta_totales = """
                SELECT
                    COUNT(DISTINCT e.nie) AS total_asistidos,
                    COUNT(DISTINCT CASE WHEN est.genero = 'M' AND e.nie IS NOT NULL THEN e.nie END) AS total_masculino,
                    COUNT(DISTINCT CASE WHEN est.genero = 'F' AND e.nie IS NOT NULL THEN e.nie END) AS total_femenino,
                    COUNT(CASE WHEN e.nie IS NULL THEN 1 END) AS total_inasistidos,
                    ROUND(100.0 * COUNT(DISTINCT e.nie) / NULLIF(COUNT(DISTINCT e.nie) + COUNT(CASE WHEN e.nie IS NULL THEN 1 END), 0), 2) AS porcentaje_asistencia
                FROM estudiantes est
                LEFT JOIN entrada e ON est.nie = e.nie
                JOIN seccion sec ON est.año = sec.año AND est.seccion = sec.seccion
                WHERE est.genero IN ('M', 'F')
                AND CONCAT(sec.año, sec.seccion) LIKE %s
            """

            cursor.execute(consulta_totales, tuple(params_detalle))
            totales = cursor.fetchone()

            # Obtener los estudiantes que no asistieron
            consulta_inasistentes = """
                SELECT
                    est.nombre, est.nie
                FROM estudiantes est
                LEFT JOIN entrada e ON est.nie = e.nie
                WHERE (e.nie IS NULL OR TIME(e.hora_entrada) BETWEEN '12:45:00' AND '21:00:00')
                AND est.año = %s AND est.seccion = %s
            """

            cursor.execute(consulta_inasistentes, (anio, seccion))
            estudiantes_no_asistieron = cursor.fetchall()

        # Agregar los detalles de la fecha y día de la semana
        for record in resumen:
            record['fecha'] = record['fecha_entrada'].strftime('%Y-%m-%d') if record['fecha_entrada'] else date.today().strftime('%Y-%m-%d')
            record['dia_semana'] = record['fecha_entrada'].strftime('%A') if record['fecha_entrada'] else date.today().strftime('%A')

        return render_template('detalles.html', resumen=resumen, totales=totales, anio=anio, seccion=seccion,
                               estudiantes_no_asistieron=estudiantes_no_asistieron)

    except Exception as e:
        print(f"Error: {str(e)}")
        flash("Ocurrió un error al procesar los datos.", "danger")
        return render_template('detalles.html', resumen=[], totales={}, anio=anio, seccion=seccion)

    finally:
        if conn:
            conn.close()
