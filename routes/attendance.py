from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from models.database import db_operation
from datetime import datetime, time as dt_time

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/asistencia', methods=['GET', 'POST'])
@db_operation
def asistencia_router(cursor):
    if request.method == 'POST':
        nie_estudiante = request.form['nie']

        try:
            cursor.execute("SELECT * FROM estudiantes WHERE nie = %s", (nie_estudiante,))
            estudiante = cursor.fetchone()

            if estudiante:
                fecha_actual = datetime.now().date()
                hora_actual = datetime.now().time()

                # Verificar si ya existe una entrada en el mismo minuto
                cursor.execute("""
                    SELECT * FROM entrada 
                    WHERE nie = %s AND fecha_entrada = %s AND EXTRACT(MINUTE FROM hora_entrada) = EXTRACT(MINUTE FROM %s)
                """, (nie_estudiante, fecha_actual, hora_actual))
                entrada_existente = cursor.fetchone()

                if entrada_existente:
                    flash('Ya existe una entrada registrada en el mismo minuto.', 'warning')
                else:
                    # Comprobar si la entrada fue registrada entre las 6 y las 13:00
                        cursor.execute(
                            "INSERT INTO entrada (nie, fecha_entrada, hora_entrada) VALUES (%s, %s, %s)",
                            (nie_estudiante, fecha_actual, hora_actual)
                        )
                        flash('Asistencia registrada con éxito.', 'success')
            else:
                flash('El estudiante con ese NIE no existe.', 'danger')

        except Exception as e:
            flash(f'Ocurrió un error: {str(e)}', 'danger')

        return redirect(url_for('attendance.asistencia_router'))

    return render_template('/asistencia.html')

@attendance_bp.route('/registrar_entrada_automatica', methods=['POST'])
@db_operation
def registrar_entrada_automatica(cursor):
    fecha_actual = datetime.now().date()
    hora_automatica = dt_time(13, 16)

    try:
        # Seleccionar estudiantes que registraron entrada entre las 6:00 y las 12:00
        # y que no tienen una salida registrada en el mismo día
        cursor.execute("""
            SELECT nie 
            FROM entrada 
            WHERE fecha_entrada = %s AND hora_entrada BETWEEN %s AND %s
            AND nie NOT IN (
                SELECT nie 
                FROM salida 
                WHERE fecha_salida = %s
            )
        """, (fecha_actual, dt_time(6, 0), dt_time(21, 00), fecha_actual))
        
        estudiantes_sin_salida = cursor.fetchall()

        # Insertar entrada automática para cada estudiante que cumple las condiciones
        for estudiante in estudiantes_sin_salida:
            cursor.execute(
                "INSERT INTO entrada (nie, fecha_entrada, hora_entrada) VALUES (%s, %s, %s)",
                (estudiante['nie'], fecha_actual, hora_automatica)
            )

        return jsonify({"message": "Entradas automáticas registradas correctamente."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@attendance_bp.route('/salida', methods=['GET', 'POST'])
@db_operation
def salida_router(cursor):
    if request.method == 'POST':
        nie_estudiante = request.form['nie']

        try:
            cursor.execute("SELECT * FROM estudiantes WHERE nie = %s", (nie_estudiante,))
            estudiante = cursor.fetchone()

            if estudiante:
                # Fecha y hora para registrar la salida
                fecha_actual = datetime.now().date()
                hora_actual = datetime.now().time()

                # Verificar si ya existe una salida en el mismo minuto
                cursor.execute("""
                    SELECT * FROM salida 
                    WHERE nie = %s AND fecha_salida = %s AND EXTRACT(MINUTE FROM hora_salida) = EXTRACT(MINUTE FROM %s)
                """, (nie_estudiante, fecha_actual, hora_actual))
                salida_existente = cursor.fetchone()

                if salida_existente:
                    flash('Ya existe una salida registrada en el mismo minuto.', 'warning')
                else:
                    cursor.execute(
                        "INSERT INTO salida (nie, fecha_salida, hora_salida) VALUES (%s, %s, %s)",
                        (nie_estudiante, fecha_actual, hora_actual)
                    )
                    flash('Salida registrada con éxito.', 'success')
            else:
                flash('El estudiante con ese NIE no existe.', 'danger')

        except Exception as e:
            flash(f'Ocurrió un error: {str(e)}', 'danger')

        return redirect(url_for('attendance.salida_router'))

    return render_template('/salida.html', web_name='Salida')