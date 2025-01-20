from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from config.config import Config
from routes.students import students_bp
from routes.attendance import attendance_bp
from routes.sections import sections_bp
from routes.admintarde import admintarde_bp
from routes.verasitencia import verasitencia_bp
from routes.admin_mañana import admin_mañana_bp
from routes.registro_automatico import llamar_registro_automatico
from routes.login import login_bp , inicio_bp
from routes.informe import informe_bp
from routes.informeAM import informeAM_bp
from routes.inicio import index_bp
from routes.aula import aula_bp
from routes.aula_pm import aulapm_bp
from routes.asistencias import asistencias_bp
from routes.materias import asistencias_class_bp
import threading
import os



# Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'ADN INA'  # Configura la clave secreta para la sesión

# Registrar los blueprints
app.register_blueprint(students_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(sections_bp)
app.register_blueprint(admintarde_bp)
app.register_blueprint(admin_mañana_bp)
app.register_blueprint(login_bp)
app.register_blueprint(inicio_bp)
app.register_blueprint(index_bp)
app.register_blueprint(aula_bp)
app.register_blueprint(aulapm_bp)
app.register_blueprint(asistencias_bp)
app.register_blueprint(asistencias_class_bp)



app.register_blueprint(informe_bp, url_prefix='/informe')
app.register_blueprint(informeAM_bp, url_prefix='/informeAM')

app.register_blueprint(verasitencia_bp)

@app.errorhandler(404)
def page_not_found(error):
    # Puedes personalizar el mensaje de error y devolver una plantilla
    return render_template("error404.html")



# Función para iniciar el hilo de la tarea de registro automático
def iniciar_registro_automatico():
    threading.Thread(target=llamar_registro_automatico, daemon=True).start()

# Ejecutar el hilo después de que Flask inicie la aplicación
if __name__ == '__main__':
    iniciar_registro_automatico()
    app.run(debug=True, host='0.0.0.0', port=5000)
