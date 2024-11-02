# routes/attendance.py
from flask import Blueprint, request, flash, redirect, url_for, render_template
from models.database import db_operation
from datetime import datetime

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
                cursor.execute(
                    "INSERT INTO entrada (nie, fecha, hora) VALUES (%s, %s, %s)",
                    (nie_estudiante, fecha_actual, hora_actual)
                )
                flash('Asistencia registrada con éxito.', 'success')
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
                fecha_actual = datetime.now().date()
                hora_actual = datetime.now().time()
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