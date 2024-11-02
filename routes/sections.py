from flask import Blueprint, request, flash, redirect, url_for, render_template
from models.database import db_operation

sections_bp = Blueprint('sections', __name__)

@sections_bp.route('/secciones', methods=['GET', 'POST'])
@db_operation
def secciones_router(cursor):
    if request.method == 'POST':
        seccion = request.form['seccion']
        año = request.form['año']
        especialidad = request.form['especialidad']
 
        try:
            cursor.execute(
                "INSERT INTO seccion (seccion, año, especialidad ) VALUES (%s, %s, %s)",
                (seccion, año, especialidad)
            )
            flash('Sección registrada con éxito.', 'success')
        except Exception as e:
            flash(f'Error al registrar sección: {e}', 'danger')
            
        return redirect(url_for('sections.secciones_router'))

    return render_template('/secciones.html')