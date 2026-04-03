"""
FnB - Student Routes Module
Author: Shashi
SRS Reference: Section 4.2 - Project Submission & Review (Student side)
REQ-4.2.1 (Submit), REQ-4.2.2 (Store+Associate), REQ-4.2.6 (View own feedback only)
D-SQ-02: Student Project Submission
D-SQ-04: Student Views Personalized Feedback
D-SEC-07: Data Access Isolation (student_id filter)
D-SEC-08: Secure File Uploads
"""

import os
from datetime import datetime
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, current_app)
from werkzeug.utils import secure_filename
from routes.auth_routes import login_required, role_required
from models.project_model import ProjectModel
from models.feedback_model import FeedbackModel

student_bp = Blueprint('student', __name__, url_prefix='/student')

ALLOWED_EXTENSIONS = {'pdf', 'zip', 'png', 'jpg', 'txt', 'py', 'html', 'docx'}


def allowed_file(filename):
    """Validate file extension – D-SEC-08"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── Student Dashboard ────────────────────────────────────────────────────────

@student_bp.route('/dashboard')
@role_required('student')
def dashboard():
    """
    Student home page showing their submitted projects.
    REQ-4.2.2: Projects associated with this student only.
    D-SEC-07: student_id filter enforced.
    """
    projects = ProjectModel.get_by_student(session['user_id'])
    return render_template('student/dashboard.html',
                           projects=projects,
                           username=session.get('username'))


# ─── Submit Project ───────────────────────────────────────────────────────────

@student_bp.route('/submit', methods=['GET', 'POST'])
@role_required('student')
def submit_project():
    """
    Allows student to submit a new project with metadata and optional file.
    REQ-4.2.1, D-SQ-02: validateInput() → new Project() → submit() → insert doc
    D-SEC-08: Secure file upload, filename sanitized via werkzeug.
    """
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        tech_stack  = request.form.get('tech_stack', '').strip()
        usp         = request.form.get('usp', '').strip()
        innovation  = request.form.get('innovation_level', 'medium')

        # Server-side validation – D-SEC-05
        errors = []
        if not title:
            errors.append('Project title is required.')
        if not description:
            errors.append('Project description is required.')
        if not tech_stack:
            errors.append('Technology stack is required.')
        if innovation not in ['low', 'medium', 'high']:
            innovation = 'medium'

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('student/submit_project.html')

        # Handle file upload – D-SEC-08
        file_path = None
        file = request.files.get('project_file')
        if file and file.filename:
            if not allowed_file(file.filename):
                flash('Invalid file type. Allowed: pdf, zip, png, jpg, txt, py, html, docx', 'error')
                return render_template('student/submit_project.html')
            safe_name = secure_filename(file.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            unique_name = f"{session['user_id']}_{timestamp}_{safe_name}"
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
            file.save(save_path)
            file_path = unique_name  # Store relative name only, never web-accessible directly

        # Save to MongoDB via Manav's model
        ProjectModel.create_project(
            student_id=session['user_id'],
            title=title,
            description=description,
            tech_stack=tech_stack,
            usp=usp,
            innovation_level=innovation,
            file_path=file_path
        )

        flash('Project submitted successfully! Wait for teacher feedback.', 'success')
        return redirect(url_for('student.dashboard'))

    return render_template('student/submit_project.html')


# ─── View My Feedback ─────────────────────────────────────────────────────────

@student_bp.route('/my-feedback')
@role_required('student')
def my_feedback():
    """
    Shows personalized feedback for logged-in student only.
    REQ-4.2.6, REQ-4.3.2: Only own feedback shown.
    D-SQ-04: enforceRole(Student) → getForStudent(session.user_id) → find(student_id)
    D-SEC-07: student_id == session.user_id enforced in query.
    """
    feedbacks = FeedbackModel.get_for_student(session['user_id'])
    return render_template('student/my_feedback.html',
                           feedbacks=feedbacks,
                           username=session.get('username'))
