# routes/admin.py
from flask import Blueprint, request, flash, redirect, url_for, render_template
from models.database import db_operation, get_db_connection
from utils.pdf_generator import AttendanceReport
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/administracionM', methods=['GET', 'POST'])
def administracion():
    try:
        conn = get_db_connection()
        if not conn:
            flash("No se pudo conectar a la base de datos.", "danger")
            return render_template('administracion.html', asistencias_hoy=[], salidas_hoy=[], 
                                conteo_genero=[], resumen=[], busqueda='', fecha_inicio='', fecha_fin='')

        asistencias_hoy = []
        salidas_hoy = []
        conteo_genero = [] 
        resumen = []
        busqueda = ''
        fecha_inicio = ''
        fecha_fin = ''

        if request.method == 'POST':
            busqueda = request.form.get('busqueda', '').strip()
            fecha_inicio = request.form.get('fecha_inicio')
            fecha_fin = request.form.get('fecha_fin')
            descargar_pdf = request.form.get('descargar_pdf')

            try:
                fecha_actual = datetime.now().date()
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date() if fecha_inicio else fecha_actual
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else fecha_actual


                if fecha_fin < fecha_inicio:
                    flash("La fecha final no puede ser menor que la fecha inicial.", "warning")
                    fecha_fin = fecha_inicio

            except ValueError:
                flash("Formato de fecha inválido. Usando fecha actual.", "warning")
                fecha_inicio = fecha_actual
                fecha_fin = fecha_actual

            try:
                with conn.cursor() as cursor:


                #Consulta para obtener las entradas , con JOIN
                    query_entradas = """
                        SELECT 
                            e.nombre,
                            e.codigo,
                            e.nie,
                            e.genero,
                            ent.id_entrada,
                            ent.fecha,
                            ent.hora
                        FROM entrada ent
                        JOIN estudiantes e ON ent.nie = e.nie
                        WHERE (e.nie LIKE %s OR e.codigo LIKE %s)
                        AND DATE(ent.fecha) BETWEEN %s AND %s
                        ORDER BY ent.fecha DESC, ent.hora DESC
                    """
                    cursor.execute(query_entradas,
                                 ('%' + busqueda + '%', '%' + busqueda + '%', 
                                  fecha_inicio, fecha_fin))
                    asistencias_hoy = cursor.fetchall()


                    #consulta para obtener las salidas , combinando las tablas con JOIN
                    query_salidas = """
                        SELECT 
                            e.nombre,
                            e.codigo,
                            e.nie,
                            e.genero,
                            sal.id_salida,
                            sal.fecha,
                            sal.hora
                        FROM salida sal
                        JOIN estudiantes e ON sal.nie = e.nie
                        WHERE (e.nie LIKE %s OR e.codigo LIKE %s)
                        AND DATE(sal.fecha) BETWEEN %s AND %s
                        ORDER BY sal.fecha DESC, sal.hora DESC
                    """
                    cursor.execute(query_salidas,
                                 ('%' + busqueda + '%', '%' + busqueda + '%', 
                                  fecha_inicio, fecha_fin))
                    salidas_hoy = cursor.fetchall()

                    #consulta para el conteo de genero

                    query_count_genero = """
                        SELECT 
                            UPPER(e.genero) AS genero_normalizado,
                            COUNT(*) AS total
                        FROM entrada ent
                        JOIN estudiantes e ON ent.nie = e.nie
                        WHERE (e.nie LIKE %s OR e.codigo LIKE %s)
                        AND DATE(ent.fecha) BETWEEN %s AND %s
                        GROUP BY genero_normalizado
                    """
                    cursor.execute(query_count_genero,
                                ('%' + busqueda + '%', '%' + busqueda + '%', 
                                    fecha_inicio, fecha_fin))
                    conteo_genero = cursor.fetchall()
                    if not asistencias_hoy and not salidas_hoy and busqueda:
                        flash("No se encontraron registros para la búsqueda especificada.", "info")

                    consulta = """
                        SELECT 
                            sec.año, 
                            sec.seccion, 
                            COUNT(e.nie) AS total_asistidos,
                            COUNT(CASE WHEN est.genero = 'M' AND e.nie IS NOT NULL THEN 1 END) AS total_masculino,
                            COUNT(CASE WHEN est.genero = 'F' AND e.nie IS NOT NULL THEN 1 END) AS total_femenino,
                            COUNT(CASE WHEN e.nie IS NULL THEN 1 END) AS total_inasistidos,
                            GROUP_CONCAT(CASE WHEN e.nie IS NULL THEN est.codigo END) AS codigos_inasistidos,
                            GROUP_CONCAT(CASE WHEN e.nie IS NOT NULL THEN est.codigo END) AS codigos_asistidos
                        FROM estudiantes est
                        LEFT JOIN entrada e ON est.nie = e.nie AND DATE(e.fecha) BETWEEN %s AND %s
                        JOIN seccion sec ON est.año = sec.año AND est.seccion = sec.seccion
                        WHERE est.genero IN ('M', 'F')  -- Filtrar solo M y F
                        GROUP BY sec.año, sec.seccion
                    """



                    cursor.execute(consulta, (fecha_inicio, fecha_fin))
                    resumen = cursor.fetchall()


            except Exception as e:
                print(f"Error en la consulta: {str(e)}")
                flash("Error al consultar la base de datos.", "danger")
                return render_template('administracion.html', 
                                    asistencias_hoy=[], 
                                    salidas_hoy=[],
                                    conteo_genero=[],
                                    resumen=[],
                                    busqueda=busqueda,
                                    fecha_inicio=fecha_inicio,
                                    fecha_fin=fecha_fin)

            #para descargar el pdf
            if descargar_pdf:
                try:
                    # Supongamos que asistencias_hoy y salidas_hoy son listas de diccionarios
                    report = AttendanceReport(asistencias_hoy, salidas_hoy)
                    return report.generate()  # Llama al método para generar el PDF
                except Exception as e:
                    print(f"Error al generar PDF: {str(e)}")
                    flash("Error al generar el PDF.", "danger")

    except Exception as e:
        print(f"Error general: {str(e)}")
        flash("Ocurrió un error inesperado.", "danger")
        return render_template('administracion.html', 
                             asistencias_hoy=[], 
                             salidas_hoy=[],
                             conteo_genero=[],
                             resumen=[],
                             busqueda='',
                             fecha_inicio='',
                             fecha_fin='')

    finally:
        if conn:
            conn.close()

    #envia los datos al template
    return render_template('administracion.html',
                         asistencias_hoy=asistencias_hoy,
                         salidas_hoy=salidas_hoy,
                         conteo_genero=conteo_genero,  
                         resumen = resumen,
                         busqueda=busqueda,
                         fecha_inicio=fecha_inicio,
                         fecha_fin=fecha_fin)

