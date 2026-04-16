"""
FnB - Teacher Routes Module
Author: Shashi
SRS Reference: Section 4.2 - Project Review, Section 4.3 - Feedback Management
REQ-4.2.3 (View projects), REQ-4.2.4 (Provide feedback)
REQ-4.2.5 (Filter projects), REQ-4.3.3 (Update feedback)
D-SQ-03: Teacher Reviews Project and Provides Feedback
D-CL-02: Project.filterByQuality/Tech/USP/Innovation()
D-CL-03: Feedback.save(), Feedback.update()
"""

from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, send_from_directory, current_app)
from datetime import datetime
import os
from routes.auth_routes import role_required
from models.project_model import ProjectModel
from models.feedback_model import FeedbackModel
from models.user_model import UserModel

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')


# ─── Teacher Dashboard ────────────────────────────────────────────────────────

@teacher_bp.route('/dashboard')
@role_required('teacher')
def dashboard():
    """Teacher home showing summary stats."""
    total_projects  = ProjectModel.count_all()
    pending         = ProjectModel.count_by_status('pending')
    reviewed        = ProjectModel.count_by_status('reviewed')
    return render_template('teacher/dashboard.html',
                           username=session.get('username'),
                           total_projects=total_projects,
                           pending=pending,
                           reviewed=reviewed)


# ─── Project List with Filters ────────────────────────────────────────────────

@teacher_bp.route('/projects')
@role_required('teacher')
def project_list():
    """
    Teacher views all submitted projects with optional filters.
    REQ-4.2.3, REQ-4.2.5: filter by quality, innovation, tech_stack, usp
    D-SQ-03: filter(quality/tech/usp) → project list
    D-CL-02: filterByQuality(), filterByTech(), filterByUSP(), filterByInnovation()
    """
    # Read filter params from query string
    tech_filter        = request.args.get('tech_stack', '').strip()
    innovation_filter  = request.args.get('innovation_level', '').strip()
    status_filter      = request.args.get('status', '').strip()

    filters = {}
    if tech_filter:
        filters['tech_stack'] = tech_filter
    if innovation_filter and innovation_filter in ['low', 'medium', 'high']:
        filters['innovation_level'] = innovation_filter
    if status_filter and status_filter in ['pending', 'reviewed']:
        filters['status'] = status_filter

    projects = ProjectModel.get_all_filtered(filters)

    return render_template('teacher/project_list.html',
                           projects=projects,
                           username=session.get('username'),
                           tech_filter=tech_filter,
                           innovation_filter=innovation_filter,
                           status_filter=status_filter)


# ─── Project Detail ───────────────────────────────────────────────────────────

@teacher_bp.route('/projects/<project_id>')
@role_required('teacher')
def project_detail(project_id):
    """
    View full details of a single project.
    REQ-4.2.3: Teacher views project detail.
    D-SQ-03: getDetails() → project detail page
    """
    project = ProjectModel.get_by_id(project_id)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('teacher.project_list'))

    # Get student info
    student = UserModel.find_by_id(str(project['student_id']))

    # Get existing feedback if any
    existing_feedback = FeedbackModel.get_for_project(project_id)

    return render_template('teacher/project_detail.html',
                           project=project,
                           student=student,
                           existing_feedback=existing_feedback,
                           username=session.get('username'))


# ─── Download Project File ───────────────────────────────────────────────────

@teacher_bp.route('/download/<path:filename>')
@role_required('teacher')
def download_file(filename):
    """
    Serves uploaded project files to teachers for review.
    REQ-4.2.3: Teacher views project details including submitted files.
    D-SEC-08: Files served through Flask (not directly web-accessible).
    Only teachers (authenticated + role_required) can access this route.
    """
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename, as_attachment=False)


# ─── Give / Update Feedback ───────────────────────────────────────────────────

@teacher_bp.route('/projects/<project_id>/feedback', methods=['GET', 'POST'])
@role_required('teacher')
def give_feedback(project_id):
    """
    Teacher provides or updates feedback for a project.
    REQ-4.2.4, REQ-4.3.1, REQ-4.3.3
    D-SQ-03: new Feedback(data) → save() → update Project.status=reviewed
    D-CL-03: Feedback.save(), Feedback.update()
    """
    project = ProjectModel.get_by_id(project_id)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('teacher.project_list'))

    existing_feedback = FeedbackModel.get_for_project(project_id)

    if request.method == 'POST':
        remarks           = request.form.get('remarks', '').strip()
        suggestions       = request.form.get('suggestions', '').strip()
        improvement_notes = request.form.get('improvement_notes', '').strip()
        quality_rating    = request.form.get('quality_rating', '').strip()

        if not remarks:
            flash('Remarks field is required.', 'error')
            return render_template('teacher/give_feedback.html',
                                   project=project,
                                   existing_feedback=existing_feedback,
                                   username=session.get('username'))

        # Validate quality rating
        try:
            quality_rating = int(quality_rating)
            if quality_rating < 1 or quality_rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            quality_rating = None

        if existing_feedback:
            # Update existing feedback – REQ-4.3.3, Feedback.update()
            FeedbackModel.update_feedback(
                feedback_id=str(existing_feedback['_id']),
                remarks=remarks,
                suggestions=suggestions,
                improvement_notes=improvement_notes
            )
            if quality_rating:
                ProjectModel.update_quality_rating(project_id, quality_rating)
            flash('Feedback updated successfully!', 'success')
        else:
            # Create new feedback – REQ-4.3.1, Feedback.save()
            FeedbackModel.create_feedback(
                project_id=project_id,
                teacher_id=session['user_id'],
                student_id=str(project['student_id']),
                remarks=remarks,
                suggestions=suggestions,
                improvement_notes=improvement_notes
            )
            # Update project status to 'reviewed' – D-SQ-03
            ProjectModel.update_status(project_id, 'reviewed')
            if quality_rating:
                ProjectModel.update_quality_rating(project_id, quality_rating)
            flash('Feedback submitted successfully!', 'success')

        return redirect(url_for('teacher.project_detail', project_id=project_id))

    return render_template('teacher/give_feedback.html',
                           project=project,
                           existing_feedback=existing_feedback,
                           username=session.get('username'))
