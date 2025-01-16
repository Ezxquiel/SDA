
# routes.py
import pymysql 
from flask import Blueprint, request, flash, redirect, url_for, render_template, send_file, session
from models.database import db_operation, get_db_connection
from datetime import datetime, date
from utils.pdf_generator import AttendanceReport



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
                    # Consulta principal simplificada
                    consulta_detalle = """
                        SELECT 
                            sec.año,
                            sec.seccion,
                            DATE(e.fecha_entrada) as fecha_entrada,
                            COUNT(DISTINCT e.nie) as total_asistidos,
                            SUM(CASE WHEN est.genero = 'M' THEN 1 ELSE 0 END) as total_masculino,
                            SUM(CASE WHEN est.genero = 'F' THEN 1 ELSE 0 END) as total_femenino,
                            (
                                SELECT COUNT(est2.nie)
                                FROM estudiantes est2
                                WHERE est2.año = sec.año 
                                AND est2.seccion = sec.seccion
                                AND est2.nie NOT IN (
                                    SELECT nie 
                                    FROM entrada
                                    WHERE DATE(fecha_entrada) = DATE(e.fecha_entrada)
                                    AND TIME(hora_entrada) BETWEEN '12:01:00' AND '19:00:00'
                                )
                            ) as total_inasistidos,
                            (
                                SELECT GROUP_CONCAT(est2.codigo)
                                FROM estudiantes est2
                                WHERE est2.año = sec.año 
                                AND est2.seccion = sec.seccion
                                AND est2.nie NOT IN (
                                    SELECT nie 
                                    FROM entrada
                                    WHERE DATE(fecha_entrada) = DATE(e.fecha_entrada)
                                    AND TIME(hora_entrada) BETWEEN '12:01:00' AND '19:00:00'
                                )
                            ) as codigos_inasistidos
                        FROM estudiantes est
                        JOIN seccion sec ON est.año = sec.año AND est.seccion = sec.seccion
                        LEFT JOIN entrada e ON est.nie = e.nie 
                            AND DATE(e.fecha_entrada) BETWEEN %s AND %s
                            AND TIME(e.hora_entrada) BETWEEN '12:01:00' AND '19:00:00'
                        WHERE e.nie IS NOT NULL
                        AND est.genero IN ('M', 'F')
                        {0}
                        GROUP BY sec.año, sec.seccion, DATE(e.fecha_entrada)
                        ORDER BY sec.año, sec.seccion, fecha_entrada
                    """.format("AND CONCAT(sec.año, sec.seccion) LIKE %s" if busqueda else "")


                    # Consulta de totales simplificada
                    consulta_totales = """
                        SELECT 
                            COUNT(DISTINCT e.nie) as total_asistidos,
                            SUM(CASE WHEN est.genero = 'M' AND e.nie IS NOT NULL THEN 1 ELSE 0 END) as total_masculino,
                            SUM(CASE WHEN est.genero = 'F' AND e.nie IS NOT NULL THEN 1 ELSE 0 END) as total_femenino,
                            (
                                SELECT COUNT(est2.nie)
                                FROM estudiantes est2
                                WHERE est2.nie NOT IN (
                                    SELECT nie 
                                    FROM entrada
                                    WHERE DATE(fecha_entrada) BETWEEN %s AND %s
                                )
                            ) as total_inasistidos
                        FROM estudiantes est
                        LEFT JOIN entrada e ON est.nie = e.nie 
                            AND DATE(e.fecha_entrada) BETWEEN %s AND %s
                            AND TIME(e.hora_entrada) BETWEEN '12:01:00' AND '19:00:00'
                        WHERE est.genero IN ('M', 'F')
                        {0}
                    """.format("AND CONCAT(est.año, est.seccion) LIKE %s" if busqueda else "")

                    # Preparar parámetros
                    params_detalle = [fecha_inicio, fecha_fin]
                    params_totales = [fecha_inicio, fecha_fin, fecha_inicio, fecha_fin]
                    
                    if busqueda:
                        params_detalle.append(f"%{busqueda}%")
                        params_totales.append(f"%{busqueda}%")

                    # Ejecutar consultas
                    cursor.execute(consulta_detalle, tuple(params_detalle))
                    resumen = cursor.fetchall()
                    
                    cursor.execute(consulta_totales, tuple(params_totales))
                    totales = cursor.fetchone()

                    # Procesar los resultados para calcular porcentajes
                    if resumen:
                        for row in resumen:
                            total = row['total_asistidos'] + row['total_inasistidos']
                            row['porcentaje_asistencia'] = round((row['total_asistidos'] / total * 100), 2) if total > 0 else 0

                    if totales:
                        total = totales['total_asistidos'] + totales['total_inasistidos']
                        totales['porcentaje_asistencia'] = round((totales['total_asistidos'] / total * 100), 2) if total > 0 else 0

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

    # Add the date and day of the week to each record
    for record in resumen:
        if record['fecha_entrada']:
            record['fecha'] = record['fecha_entrada'].strftime('%Y-%m-%d')
            record['dia_semana'] = record['fecha_entrada'].strftime('%A')
        else:
            record['fecha'] = fecha_inicio.strftime('%Y-%m-%d')
            record['dia_semana'] = fecha_inicio.strftime('%A')

    return render_template('vespertino.html', resumen=resumen, totales=totales, busqueda=busqueda, 
                         fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, web_name='Vespertino')
