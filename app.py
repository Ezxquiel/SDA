from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from config.config import Config
from routes.students import students_bp
from routes.attendance import attendance_bp
from routes.admin import admin_bp
from routes.sections import sections_bp
from routes.admintarde import admintarde_bp
from routes.verasitencia import sections_bp
from routes.admin_mañana import admin_mañana_bp
from routes.registro_automatico import llamar_registro_automatico
from routes.login import login_bp , inicio_bp
from routes.informe import informe_bp
from routes.inicio import index_bp
import threading
import os



# Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'tu_clave_secreta_aqui'  # Configura la clave secreta para la sesión

# Registrar los blueprints
app.register_blueprint(students_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(sections_bp)
app.register_blueprint(admintarde_bp)
app.register_blueprint(admin_mañana_bp)
app.register_blueprint(login_bp)
app.register_blueprint(inicio_bp)
app.register_blueprint(index_bp)
app.register_blueprint(informe_bp, url_prefix='/informe')

# Función para iniciar el hilo de la tarea de registro automático
def iniciar_registro_automatico():
    threading.Thread(target=llamar_registro_automatico, daemon=True).start()

# Ejecutar el hilo después de que Flask inicie la aplicación
if __name__ == '__main__':
    iniciar_registro_automatico()
    app.run(debug=True, host='0.0.0.0', port=5000)
