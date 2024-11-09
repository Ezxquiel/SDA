# routes/attendance.py
from flask import Blueprint, request, flash, redirect, url_for, render_template
from models.database import db_operation
from datetime import datetime, time, timedelta
import time

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/asistencia', methods=['GET', 'POST'])
@db_operation
def asistencia_router(cursor):
    if request.method == 'POST':
        nie_estudiante = request.form['nie']
        
        try:
            # Verificar si el estudiante existe
            cursor.execute("SELECT * FROM estudiantes WHERE nie = %s", (nie_estudiante,))
            estudiante = cursor.fetchone()
            
            if estudiante:
                fecha_actual = datetime.now().date()
                hora_actual = datetime.now().time()

                # Comprobar si la entrada fue registrada entre las 6 y las 12 de la mañana
                if time(6, 0) <= hora_actual <= time(13, 0):
                    cursor.execute(
                        "INSERT INTO entrada (nie, fecha, hora) VALUES (%s, %s, %s)",
                        (nie_estudiante, fecha_actual, hora_actual)
                    )
                    flash('Asistencia registrada con éxito.', 'success')

                # Verificar si el estudiante tiene una salida antes de la 1:15 p.m.
                cursor.execute(
                    "SELECT * FROM salida WHERE nie = %s AND fecha = %s AND hora <= %s",
                    (nie_estudiante, fecha_actual, time(13, 15))
                )
                salida_registrada = cursor.fetchone()

                if not salida_registrada:
                    # Si no hay salida antes de la 1:15 p.m., insertar una entrada automática a las 1:16 p.m.
                    cursor.execute(
                        "INSERT INTO entrada (nie, fecha, hora) VALUES (%s, %s, %s)",
                        (nie_estudiante, fecha_actual, time(13, 16))
                    )
                    flash('Entrada automática registrada a las 1:16 p.m.', 'info')

            else:
                flash('El estudiante con ese NIE no existe.', 'danger')
        
        except Exception as e:
            flash(f'Ocurrió un error: {str(e)}', 'danger')
        
        return redirect(url_for('attendance.asistencia_router'))

    return render_template('/asistencia.html')


@attendance_bp.route('/salida', methods=['GET', 'POST'])
@db_operation
def salida_router(cursor):
    if request.method == 'POST':
        nie_estudiante = request.form['nie']
        
        try:
            cursor.execute("SELECT * FROM estudiantes WHERE nie = %s", (nie_estudiante,))
            estudiante = cursor.fetchone()
            
            if estudiante:
                # Fecha y hora de prueba para salida
                fecha_actual = datetime.now().date()
                hora_actual = datetime.now().time()

                # Registrar salida
                cursor.execute(
                    "INSERT INTO salida (nie, fecha, hora) VALUES (%s, %s, %s)",
                    (nie_estudiante, fecha_actual, hora_actual)
                )
                flash('Salida registrada con éxito.', 'success')

            else:
                flash('El estudiante con ese NIE no existe.', 'danger')
        
        except Exception as e:
            flash(f'Ocurrió un error: {str(e)}', 'danger')
        
        return redirect(url_for('attendance.salida_router'))

    return render_template('/salida.html')
