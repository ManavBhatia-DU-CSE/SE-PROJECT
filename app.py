# Author: Shashi
# SRS Reference: Section 5.1 - System Architecture (Three-Tier), REQ-4.1.x

import os
from flask import Flask, redirect, url_for, session
from models.db import mongo
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.admin_routes import admin_bp

# ─── App Initialization ────────────────────────────────────────────────────────
app = Flask(__name__)

# Secret key for session signing (HMAC-SHA256) – D-SEC-03
app.secret_key = 'fnb_secret_key_2026_CHANGE_IN_PRODUCTION'

# MongoDB connection string – D-DB-01, D-DB-02, D-DB-03
app.config['MONGO_URI'] = 'mongodb://localhost:27017/fnb_db'

# Secure file upload config – D-SEC-08
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'zip', 'png', 'jpg', 'txt', 'py', 'html'}

# Initialize PyMongo (Manav's db module)
mongo.init_app(app)

# ─── Register Blueprints (Application Logic Layer Modules) ─────────────────────
app.register_blueprint(auth_bp)        # /login, /register, /logout, /change-password
app.register_blueprint(student_bp)     # /student/*
app.register_blueprint(teacher_bp)     # /teacher/*
app.register_blueprint(admin_bp)       # /admin/*


# ─── Root Route ───────────────────────────────────────────────────────────────
@app.route('/')
def index():
    """Redirect to role-based dashboard or login. REQ-4.1.2, REQ-4.1.3"""
    if 'user_id' in session:
        role = session.get('role')
        if role == 'student':
            return redirect(url_for('student.dashboard'))
        elif role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        elif role == 'admin':
            return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.login'))


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
