# routes/parents.py
from flask import Blueprint, request, flash, redirect, url_for, render_template
from models.database import db_operation

parents_bp = Blueprint('parents', __name__)

@parents_bp.route('/padres', methods=['GET', 'POST'])
@db_operation
def padres_router(cursor):
    """
    Handle parent registration and display.
    Supports GET for displaying the form and POST for registering new parents.
    """
    if request.method == 'POST':
        try:
            # Extract form data
            nombre = request.form['nombre']
            numero = request.form['numero']
            correo = request.form['correo']
            dui = request.form['dui']

            # Insert new parent
            cursor.execute(
                "INSERT INTO padres (nombre, numero, correo, dui) VALUES (%s, %s, %s, %s)",
                (nombre, numero, correo, dui)
            )
            flash('Padre registrado con éxito.', 'success')
            
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:  # Duplicate entry error
                flash('Error: El DUI ya está registrado.', 'danger')
            else:
                flash(f'Error en la base de datos: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Error al registrar Padre: {str(e)}', 'danger')

        return redirect(url_for('parents.padres_router'))

    return render_template('padres.html')