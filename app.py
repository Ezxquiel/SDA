# app.py
from flask import Flask, render_template
from config.config import Config
from routes.students import students_bp
from routes.attendance import attendance_bp
from routes.admin import admin_bp
from routes.parents import parents_bp
from routes.sections import sections_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(students_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(parents_bp)
app.register_blueprint(sections_bp)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)