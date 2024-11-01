from multiprocessing.dummy import connection
from flask import Flask, request, flash, redirect, url_for, render_template, make_response
from router import routers as rt
import pymysql
from pymysql.cursors import DictCursor
from fpdf import FPDF
from functools import wraps
from datetime import datetime
import calendar 
from io import BytesIO
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) #llave random para que funcione ALV 



# Configuración de la base de datos
DB_CONFIG = {
    'host': "by8ekzvhusvvn2yqc71b-mysql.services.clever-cloud.com",
    'user': "uueyyhu8xg3oenlv",
    'password': "VFbwWo8TNmZQbg04Dd7i",
    'database': "by8ekzvhusvvn2yqc71b",
    'cursorclass': DictCursor
}

def get_db_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except pymysql.Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        return None

def db_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = get_db_connection()
        if not conn:
            flash("No se pudo conectar a la base de datos.", "danger")
            return redirect(url_for('home'))
        try:
            with conn.cursor() as cursor:
                result = func(cursor, *args, **kwargs)
            conn.commit()
            return result
        except pymysql.Error as e:
            conn.rollback()
            flash(f"Error en la base de datos: {e}", 'danger')
        finally:
            conn.close()
    return wrapper


@app.route('/')
@app.route('/home')
def home_route():
    return rt.home()  # Llamamos a la función home desde router


# UN PEDAZO DE CACA >>>>> PAWECHA 🧐

@app.route('/padres', methods=['GET', 'POST'])
@db_operation
def padres_router(cursor):
    if request.method == 'POST':
        nombre = request.form['nombre']
        numero = request.form['numero']
        correo = request.form['correo']
        dui = request.form['dui'] 

        try:
            cursor.execute(
                "INSERT INTO padres (nombre, numero, correo, dui) VALUES (%s, %s, %s, %s)",
                (nombre, numero, correo, dui)
            )
            flash('Padre registrado con éxito.', 'success')
        except Exception as e:
            flash(f'Error al registrar Padre: {e}', 'danger')

        return redirect(url_for('padres_router')) 

    return render_template('/padres.html')



@app.route('/secciones', methods=['GET', 'POST'])
@db_operation
def secciones_router(cursor):
    if request.method == 'POST':
        seccion = request.form['seccion']
        año = request.form['año']
        especialidad = request.form['especialidad']
 
        try:
            cursor.execute(
                #                *Se la INSERTA >~<*
                "INSERT INTO seccion (seccion, año, especialidad ) VALUES (%s, %s, %s)",
                (seccion, año, especialidad)
                )
            flash('alumno registrado con éxito. ', 'success')
        except Exception as e:
            flash(f'Error al registrar alumno: {e}', 'danger')
            
        return redirect(url_for('secciones_router')) 

    return render_template('/secciones.html')

@app.route('/estudiantes', methods=['GET', 'POST'])
@db_operation
def estudiantes_router(cursor):
    # Fetch available DUIs, sections, and years to populate the form
    cursor.execute("SELECT dui FROM padres")  # Fetch DUIs from parents
    duis = [row['dui'] for row in cursor.fetchall()]  # Using DictCursor

    cursor.execute("SELECT seccion FROM seccion")  # Fetch sections
    secciones = [row['seccion'] for row in cursor.fetchall()]  # Using DictCursor

    cursor.execute("SELECT DISTINCT año FROM seccion")  # Fetch distinct years
    anios = [row['año'] for row in cursor.fetchall()]  # Using DictCursor

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form['nombre']
            nie = request.form['nie']
            edad = request.form['edad']
            año = request.form['año']
            codigo = request.form['codigo']
            dui = request.form['dui']
            seccion = request.form['seccion']
            genero = request.form['genero']

            # Verificar si el padre existe
            cursor.execute("SELECT * FROM padres WHERE dui = %s", (dui,))
            padre = cursor.fetchone()
            if not padre:
                flash('El DUI del padre no está registrado.', 'danger')
                return redirect(url_for('estudiantes_router'))
            
            # Verificar si la sección existe
            cursor.execute("SELECT * FROM seccion WHERE seccion = %s AND año = %s", 
                           (seccion, año))
            seccion_exists = cursor.fetchone()
            if not seccion_exists:
                flash('La sección o año especificado no existe.', 'danger')
                return redirect(url_for('estudiantes_router'))

            # Insertar estudiante
            cursor.execute("""
                INSERT INTO estudiantes 
                (nombre, nie, edad, año, codigo, dui, seccion, genero) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, nie, edad, año, codigo, dui, seccion, genero))
            
            flash('Alumno registrado con éxito.', 'success')
            
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:  # Error de duplicado
                flash('Error: El NIE ya está registrado.', 'danger')
            else:
                flash(f'Error en la base de datos: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
            
        return redirect(url_for('estudiantes_router')) 

    return render_template('estudiantes.html', duis=duis, secciones=secciones, anios=anios)



@app.route('/asistencia', methods=['GET', 'POST'])
@db_operation
def asistencia_router(cursor):
    if request.method == 'POST':
        nie_estudiante = request.form['nie']
        
        try:
            # Verifica si el estudiante existe
                        
            cursor.execute("SELECT * FROM estudiantes WHERE nie = %s", (nie_estudiante,))
            estudiante = cursor.fetchone()
            
            if estudiante:
                # Registrar asistencia
                fecha_actual = datetime.now().date()
                hora_actual = datetime.now().time()
                cursor.execute(
                    #              *Se la INSERTA >~<*
                    "INSERT INTO entrada (nie, fecha, hora) VALUES (%s, %s, %s)",
                    (nie_estudiante, fecha_actual, hora_actual)
                )
                connection.commit() 

                flash('Asistencia registrada con éxito.', 'success')
            else:
                flash('El estudiante con ese NIE no existe.', 'danger')
        
        except Exception as e:
            flash(f'Ocurrió un error: {str(e)}', 'danger')
        
        return redirect(url_for('asistencia_router')) 

    return render_template('/asistencia.html')


@app.route('/salida', methods=['GET', 'POST'])
@db_operation
def salida_router(cursor):
    if request.method == 'POST':
        nie_estudiante = request.form['nie']
        
        try:
            # Verificar si el estudiante existe
            cursor.execute("SELECT * FROM estudiantes WHERE nie = %s", (nie_estudiante,))
            estudiante = cursor.fetchone()
            
            if estudiante:
                # Registrar asistencia
                fecha_actual = datetime.now().date()
                hora_actual = datetime.now().time()
                cursor.execute(

                            #*Se la INSERTA >~<*
                    "INSERT INTO salida (nie, fecha, hora) VALUES (%s, %s, %s)",
                    (nie_estudiante, fecha_actual, hora_actual)
                )
                connection.commit() 


                flash('Asistencia registrada con éxito.', 'success')
            else:
                flash('El estudiante con ese NIE no existe.', 'danger')
        
        except Exception as e:
            flash(f'Ocurrió un error: {str(e)}', 'danger')
        
        return redirect(url_for('salida_router')) 

    return render_template('/salida.html')

def generar_pdf(asistencias):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    p.drawString(100, height - 100, "Reporte de Asistencias")

    # Table headers
    x_offset = 50
    y_offset = height - 150
    line_height = 20
    headers = ["Nombre", "Código", "NIE", "Fecha", "Hora"]
    for i, header in enumerate(headers):
        p.drawString(x_offset + i * 100, y_offset, header)
    y_offset -= line_height

    # Table rows
    for asistencia in asistencias:
        for i, item in enumerate(asistencia):
            p.drawString(x_offset + i * 100, y_offset, str(item))
        y_offset -= line_height

    p.showPage()
    p.save()
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename="asistencias.pdf"'
    return response

@app.route('/administracion', methods=['GET', 'POST'])
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

            # Validación y formateo de fechas
            try:
                fecha_actual = datetime.now().date()
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date() if fecha_inicio else fecha_actual
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else fecha_actual

                # Validar que fecha_fin no sea menor que fecha_inicio
                if fecha_fin < fecha_inicio:
                    flash("La fecha final no puede ser menor que la fecha inicial.", "warning")
                    fecha_fin = fecha_inicio
            except ValueError:
                flash("Formato de fecha inválido. Usando fecha actual.", "warning")
                fecha_inicio = fecha_actual
                fecha_fin = fecha_actual

            try:
                with conn.cursor() as cursor:
                    # Consulta para entradas con parámetros seguros
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

                    # Consulta para salidas con parámetros seguros
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
                    return generar_pdf(asistencias_hoy, salidas_hoy)
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



def generar_pdf(entrada, salidas, mes=None, año=None):
    print("Generando PDF con asistencias:", entrada)
    print("Generando PDF con salidas:", salidas)

    # Si no se especifica mes o año, usar la fecha del primer registro
    if mes is None or año is None and entrada:
        primera_fecha = datetime.strptime(str(entrada[0]['fecha']), '%Y-%m-%d')
        mes = mes or primera_fecha.month
        año = año or primera_fecha.year
    else:
        # Si no hay registros, usar fecha actual
        ahora = datetime.now()
        mes = mes or ahora.month
        año = año or ahora.year

    pdf = FPDF()
    pdf.add_page()
    
    # Agregar marca de agua
    pdf.set_font('Arial', 'B', 50)
    pdf.set_text_color(200, 200, 200)  # Gris claro
    pdf.rotate(45, 105, 140)
    pdf.text(75, 140, 'ASISTENCIAS')
    pdf.rotate(0)
    pdf.set_text_color(0, 0, 0)  # Volver a negro

        # Agregar el logo
    logo_path = 'static/img/logoInaSinFondo.png'  # Ruta de tu imagen
    pdf.image(logo_path, x=10, y=10, w=40, h=40)  # Ajusta la posición y tamaño

    # Título del documento
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 70, 'Reporte de Asistencia'.encode('latin-1').decode('latin-1'), 0, 1, 'C')

    # Agregar calendario de asistencias
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, 'Calendario de Asistencias'.encode('latin-1').decode('latin-1'), ln=True, align='C')

    # Crear un diccionario de fechas asistidas
    fechas_asistidas = {str(entrada['fecha']): True for entrada in entrada}

    # Configurar calendario para comenzar en domingo
    calendar.setfirstweekday(calendar.SUNDAY)
    
    # Crear el calendario
    mes_cal = calendar.monthcalendar(año, mes)

    # Encabezado del mes con diseño mejorado
    pdf.set_fill_color(51, 122, 183)  # Azul corporativo
    pdf.set_text_color(255, 255, 255)  # Texto blanco
    # Usar el nombre del mes en español
    nombres_meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    nombre_mes = nombres_meses[mes].encode('latin-1').decode('latin-1')
    pdf.cell(0, 10, f"{nombre_mes} {año}", 1, 1, 'C', True)

    # Días de la semana con diseño mejorado
    pdf.set_font('Arial', 'B', 10)
    dias = ['Dom', 'Lun', 'Mar', 'Mié'.encode('latin-1').decode('latin-1'), 
            'Jue', 'Vie', 'Sáb'.encode('latin-1').decode('latin-1')]
    pdf.set_fill_color(240, 240, 240)  # Gris claro para encabezados
    pdf.set_text_color(0, 0, 0)  # Texto negro
    for dia in dias:
        pdf.cell(27, 10, dia, 1, 0, 'C', True)
    pdf.ln()

    # Contadores de días asistidos y no asistidos
    total_asistidos = 0
    total_no_asistidos = 0
    dias_habiles = 0  # Contador para días hábiles (no domingos)

    # Imprimir el calendario con diseño mejorado
    pdf.set_font('Arial', '', 10)
    for semana in mes_cal:
        for i, dia in enumerate(semana):
            if dia == 0:
                pdf.set_fill_color(245, 245, 245)  # Gris muy claro para celdas vacías
                pdf.cell(27, 10, '', 1, 0, 'C', True)
            else:
                dia_str = f"{año}-{mes:02d}-{dia:02d}"
                if i != 0:  # Si no es domingo
                    dias_habiles += 1  # Incrementar contador de días hábiles
                    if dia_str in fechas_asistidas:
                        pdf.set_fill_color(223, 240, 216)  # Verde claro para asistencias
                        pdf.set_text_color(0, 128, 0)
                        total_asistidos += 1
                    else:
                        pdf.set_fill_color(242, 222, 222)  # Rojo claro para no asistencias
                        pdf.set_text_color(169, 68, 66)
                        total_no_asistidos += 1
                else:  # Si es domingo
                    pdf.set_fill_color(220, 220, 220)  # Gris para domingos
                    pdf.set_text_color(128, 128, 128)
                
                pdf.cell(27, 10, str(dia), 1, 0, 'C', True)
                pdf.set_text_color(0, 0, 0)
        pdf.ln()

    # Agregar totales con diseño mejorado
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(63, 10, f'Días Hábiles: {dias_habiles}'.encode('latin-1').decode('latin-1'), 1, 0, 'C', True)
    pdf.cell(63, 10, f'Días Asistidos: {total_asistidos}'.encode('latin-1').decode('latin-1'), 1, 0, 'C', True)
    pdf.cell(64, 10, f'Días No Asistidos: {total_no_asistidos}'.encode('latin-1').decode('latin-1'), 1, 1, 'C', True)

    # Tablas de asistencias y salidas con diseño mejorado
    def crear_tabla(titulo, datos, es_entrada=True):
        pdf.ln(10)
        # Título de la sección
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(51, 122, 183)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(190, 10, titulo.encode('latin-1').decode('latin-1'), 1, 1, 'C', True)
        
        # Encabezados
        pdf.set_font('Arial', 'B', 8)
        pdf.set_fill_color(240, 240, 240)
        pdf.set_text_color(0, 0, 0)
        headers = [
            ('ID', 20),
            ('NIE Estudiante', 30),
            ('Nombre', 50),
            ('Fecha', 45),
            ('Hora', 45)
        ]
        
        for header, width in headers:
            pdf.cell(width, 10, header.encode('latin-1').decode('latin-1'), 1, 0, 'C', True)
        pdf.ln()
        
        # Datos
        pdf.set_font('Arial', '', 8)
        for i, dato in enumerate(datos):
            # Alternar colores de fondo para mejor legibilidad
            pdf.set_fill_color(255, 255, 255) if i % 2 == 0 else pdf.set_fill_color(245, 245, 245)
            
            id_key = 'id_entrada' if es_entrada else 'id_salida'
            pdf.cell(20, 10, str(dato[id_key]), 1, 0, 'C', True)
            pdf.cell(30, 10, str(dato['nie']), 1, 0, 'C', True)
            nombre_codificado = dato['nombre'].encode('latin-1').decode('latin-1')
            pdf.cell(50, 10, nombre_codificado, 1, 0, 'L', True)
            pdf.cell(45, 10, str(dato['fecha']), 1, 0, 'C', True)
            pdf.cell(45, 10, str(dato['hora']), 1, 1, 'C', True)

    crear_tabla('Registro de Entradas', entrada, True)
    crear_tabla('Registro de Salidas', salidas, False)

    # Agregar pie de página
    pdf.set_y(-30)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, f'Generado el {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'.encode('latin-1').decode('latin-1'), 0, 0, 'C')

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Reporte_Asistencia_Salida.pdf'
    
    return response


if __name__ == '__main__':
    app.run(debug=True)
