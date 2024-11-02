# routes/admin.py
from flask import Blueprint, request, flash, redirect, url_for, render_template
from models.database import db_operation, get_db_connection
from utils.pdf_generator import AttendanceReport
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/administracion', methods=['GET', 'POST'])
def administracion():
    try:
        conn = get_db_connection()
        if not conn:
            flash("No se pudo conectar a la base de datos.", "danger")
            return render_template('administracion.html', asistencias_hoy=[], salidas_hoy=[], 
                                busqueda='', fecha_inicio='', fecha_fin='')

        asistencias_hoy = []
        salidas_hoy = []
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

                    if not asistencias_hoy and not salidas_hoy and busqueda:
                        flash("No se encontraron registros para la búsqueda especificada.", "info")

            except Exception as e:
                print(f"Error en la consulta: {str(e)}")
                flash("Error al consultar la base de datos.", "danger")
                return render_template('administracion.html', 
                                    asistencias_hoy=[], 
                                    salidas_hoy=[],
                                    busqueda=busqueda,
                                    fecha_inicio=fecha_inicio,
                                    fecha_fin=fecha_fin)

            if descargar_pdf:
                try:
                    report = AttendanceReport(asistencias_hoy, salidas_hoy)
                    return report.generate()
                except Exception as e:
                    print(f"Error al generar PDF: {str(e)}")
                    flash("Error al generar el PDF.", "danger")

    except Exception as e:
        print(f"Error general: {str(e)}")
        flash("Ocurrió un error inesperado.", "danger")
        return render_template('administracion.html', 
                             asistencias_hoy=[], 
                             salidas_hoy=[],
                             busqueda='',
                             fecha_inicio='',
                             fecha_fin='')

    finally:
        if conn:
            conn.close()

    return render_template('administracion.html',
                         asistencias_hoy=asistencias_hoy,
                         salidas_hoy=salidas_hoy,
                         busqueda=busqueda,
                         fecha_inicio=fecha_inicio,
                         fecha_fin=fecha_fin)