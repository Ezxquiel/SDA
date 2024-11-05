from flask import Blueprint, request, flash, redirect, url_for, render_template
from models.database import db_operation, get_db_connection
from utils.pdf_generator import AttendanceReport
from datetime import datetime

admin_mañana_bp = Blueprint('admin_mañana', __name__) 

@admin_mañana_bp.route('/administracionAM', methods=['GET', 'POST'])
def administracionM():
    try:
        conn = get_db_connection()
        if not conn:
            flash("No se pudo conectar a la base de datos.", "danger")
            return render_template('matutino.html', conteo_genero=[], resumen=[], busqueda='', fecha_inicio='', fecha_fin='')

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


                    consulta = """
                        SELECT 
                            sec.año, 
                            sec.seccion, 
                            COUNT(DISTINCT e.nie) AS total_asistidos,
                            COUNT(CASE WHEN est.genero = 'M' AND e.nie IS NOT NULL THEN 1 END) AS total_masculino,
                            COUNT(CASE WHEN est.genero = 'F' AND e.nie IS NOT NULL THEN 1 END) AS total_femenino,
                            COUNT(CASE WHEN e.nie IS NULL THEN 1 END) AS total_inasistidos,
                            GROUP_CONCAT(CASE WHEN e.nie IS NULL THEN est.codigo END) AS codigos_inasistidos,
                            GROUP_CONCAT(CASE WHEN e.nie IS NOT NULL THEN est.codigo END) AS codigos_asistidos
                        FROM estudiantes est
                        LEFT JOIN entrada e ON est.nie = e.nie AND DATE(e.fecha) BETWEEN %s AND %s
                        JOIN seccion sec ON est.año = sec.año AND est.seccion = sec.seccion
                        WHERE est.genero IN ('M', 'F') 
                        AND (e.nie IS NULL OR TIME(e.hora) BETWEEN '04:00:00' AND '12:44:59')
                        GROUP BY sec.año, sec.seccion
                    """

                    cursor.execute(consulta, (fecha_inicio, fecha_fin))
                    resumen = cursor.fetchall()

            except Exception as e:
                print(f"Error en la consulta: {str(e)}")
                flash("Error al consultar la base de datos.", "danger")
                return render_template('matutino.html', 
                                    conteo_genero=[],
                                    resumen=[],
                                    busqueda=busqueda,
                                    fecha_inicio=fecha_inicio,
                                    fecha_fin=fecha_fin)

    except Exception as e:
        print(f"Error general: {str(e)}")
        flash("Ocurrió un error inesperado.", "danger")
        return render_template('matutino.html', 
                             conteo_genero=[],
                             resumen=[],
                             busqueda='',
                             fecha_inicio='',
                             fecha_fin='')


    finally:
        if conn:
            conn.close()


    #envia los datos al template
    return render_template('matutino.html',
                         conteo_genero=conteo_genero,  
                         resumen = resumen,
                         busqueda=busqueda,
                         fecha_inicio=fecha_inicio,
                         fecha_fin=fecha_fin)