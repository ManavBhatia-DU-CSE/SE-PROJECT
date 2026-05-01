# Author: Shashi
# SRS Reference: Section 5.1 - System Architecture (Three-Tier), REQ-4.1.x

import os
from flask import Flask, redirect, url_for, session
from db import mongo
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.admin_routes import admin_bp
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Only set once, from environment variable
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-dev-key')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/fnb_db')
# app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'zip', 'png', 'jpg', 'txt', 'py', 'html', 'docx'}


mongo.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'student':   return redirect(url_for('student.dashboard'))
        elif role == 'teacher': return redirect(url_for('teacher.dashboard'))
        elif role == 'admin':   return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    # UPLOAD_FOLDER removed — no local folder needed anymore
    app.run(debug=True, host='0.0.0.0', port=5000)