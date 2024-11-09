from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from config.config import Config
from routes.students import students_bp
from routes.attendance import attendance_bp
from routes.admin import admin_bp
from routes.parents import parents_bp
from routes.sections import sections_bp
from routes.admintarde import admintarde_bp
from routes.admin_mañana import admin_mañana_bp
from routes.registro_automatico import llamar_registro_automatico
import threading
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Datos de usuario y contraseña desde las variables de entorno
USUARIO = os.getenv("USUARIO")
CONTRASEÑA = os.getenv("CONTRASEÑA")

# Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'tu_clave_secreta_aqui'  # Configura la clave secreta para la sesión

# Registrar los blueprints
app.register_blueprint(students_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(parents_bp)
app.register_blueprint(sections_bp)
app.register_blueprint(admintarde_bp)
app.register_blueprint(admin_mañana_bp)

# Configurar la sesión
app.config['SESSION_PERMANENT'] = False


# Ruta principal
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')



# Función de cierre de sesión
@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login'))# Función de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        
        # Verificar credenciales
        if usuario == USUARIO and contraseña == CONTRASEÑA:
            session['usuario'] = usuario
            session['logged_in'] = True  # Estado de inicio de sesión
            flash('Has iniciado sesión correctamente.', 'success')
            # Redirigir al usuario a la página que intentaba acceder, si existe
            next_url = request.args.get('next')
            return redirect(next_url or url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Función para iniciar el hilo de la tarea de registro automático
def iniciar_registro_automatico():
    threading.Thread(target=llamar_registro_automatico, daemon=True).start()

# Ejecutar el hilo después de que Flask inicie la aplicación
if __name__ == '__main__':
    iniciar_registro_automatico()
    app.run(debug=True)
