import pymysql
from flask import Flask, render_template, request, redirect, session, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db_connection  

# Blueprints
login_bp = Blueprint('login', __name__)
inicio_bp = Blueprint('inicio', __name__)


def get_user_by_name(username):
    try:
        conn = get_db_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (username,))
            usuario = cursor.fetchone()
        conn.close()
        return usuario
    except Exception as e:
        print(f"Error getting user: {e}")
        return None



# Rutas
@inicio_bp.route('/')
def index():
    """
    Redirige a la página de inicio de sesión.
    """
    return redirect('/login')

@login_bp.route('/login', methods=["POST", "GET"])
def inicio():
    """
    Maneja la lógica de inicio de sesión.
    """
    titulo = 'Login'
    

    if request.method == "POST":
        user = request.form.get("user", "").strip()
        password = request.form.get("password", "").strip()

        # Validar usuario y contraseña
        usuario = get_user_by_name(user)
        if usuario:
            if check_password_hash(usuario["contraseña"], password):
                # Almacenar detalles del usuario en la sesión
                session['user_id'] = usuario["id"]
                session['user_name'] = usuario["nombre"]
                session['user_rango'] = usuario["rango"]
                flash(f"¡Bienvenido, {usuario['nombre']}!", "success")
                return redirect('/index')
            else:
                flash("Contraseña incorrecta", "danger")
        else:
            flash("Usuario no encontrado o deshabilitado", "danger")

    return render_template('login.html', titulo=titulo)




@login_bp.route('/logout')
def logout():
    """
    Maneja la lógica de cierre de sesión.
    """
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect('/login')
