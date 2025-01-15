from flask import Blueprint, request, flash, render_template
from models.database import get_db_connection
from datetime import datetime

asistencias_bp = Blueprint('asistencias', __name__)

@asistencias_bp.route('/consultar_asistencias', methods=['GET', 'POST'])
def consultar_asistencias():
    try:
        conn = get_db_connection()
        if not conn:
            flash("No se pudo conectar a la base de datos.", "danger")
            return render_template('asistenciaseccion.html', asistencias_hoy=[], salidas_hoy=[], busqueda='', fecha_inicio='', fecha_fin='', año='', seccion='', años=[], secciones=[])

        asistencias_hoy = {}
        salidas_hoy = {}
        busqueda = ''
        fecha_inicio = ''
        fecha_fin = ''
        año = ''
        seccion = ''
        años = []
        secciones = []

        with conn.cursor() as cursor:
            # Obtener los años únicos
            cursor.execute("SELECT DISTINCT año FROM seccion ORDER BY año")
            años = [row['año'] for row in cursor.fetchall()]

            # Obtener las secciones únicas
            cursor.execute("SELECT DISTINCT seccion FROM seccion ORDER BY seccion")
            secciones = [row['seccion'] for row in cursor.fetchall()]

        if request.method == 'POST':
            busqueda = request.form.get('busqueda', '').strip()
            fecha_inicio = request.form.get('fecha_inicio')
            fecha_fin = request.form.get('fecha_fin')
            año = request.form.get('año', '').strip()
            seccion = request.form.get('seccion', '').strip()

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
                    # Consulta para obtener las asistencias
                    query_entradas = """
                        SELECT 
                            e.nombre,
                            e.codigo,
                            e.nie,
                            e.genero,
                            ent.id_entrada,
                            ent.fecha,
                            ent.hora,
                            e.seccion
                        FROM entrada ent
                        JOIN estudiantes e ON ent.nie = e.nie
                        WHERE e.año = %s AND e.seccion = %s
                        AND DATE(ent.fecha) BETWEEN %s AND %s
                        ORDER BY ent.fecha DESC, ent.hora DESC
                    """
                    cursor.execute(query_entradas, (año, seccion, fecha_inicio, fecha_fin))
                    entradas = cursor.fetchall()

                    for entrada in entradas:
                        if entrada['seccion'] not in asistencias_hoy:
                            asistencias_hoy[entrada['seccion']] = []
                        asistencias_hoy[entrada['seccion']].append(entrada)

                    # Consulta para obtener las salidas
                    query_salidas = """
                        SELECT 
                            e.nombre,
                            e.codigo,
                            e.nie,
                            e.genero,
                            sal.id_salida,
                            sal.fecha,
                            sal.hora,
                            e.seccion
                        FROM salida sal
                        JOIN estudiantes e ON sal.nie = e.nie
                        WHERE e.año = %s AND e.seccion = %s
                        AND DATE(sal.fecha) BETWEEN %s AND %s
                        ORDER BY sal.fecha DESC, sal.hora DESC
                    """
                    cursor.execute(query_salidas, (año, seccion, fecha_inicio, fecha_fin))
                    salidas = cursor.fetchall()

                    for salida in salidas:
                        if salida['seccion'] not in salidas_hoy:
                            salidas_hoy[salida['seccion']] = []
                        salidas_hoy[salida['seccion']].append(salida)

            except Exception as e:
                print(f"Error en la consulta: {str(e)}")
                flash("Error al consultar la base de datos.", "danger")
                return render_template('asistenciaseccion.html', 
                                       asistencias_hoy={}, salidas_hoy={},
                                       busqueda=busqueda, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, año=año, seccion=seccion, años=años, secciones=secciones)

    except Exception as e:
        print(f"Error general: {str(e)}")
        flash("Ocurrió un error inesperado.", "danger")
        return render_template('asistenciaseccion.html', asistencias_hoy={}, salidas_hoy={}, busqueda='', fecha_inicio='', fecha_fin='', año='', seccion='', años=[], secciones=[])

    finally:
        if conn:
            conn.close()

    # Enviar los datos al template
    return render_template('asistenciaseccion.html', 
                           asistencias_hoy=asistencias_hoy,
                           salidas_hoy=salidas_hoy,
                           busqueda=busqueda, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, año=año, seccion=seccion, años=años, secciones=secciones)
