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


from flask import (Blueprint, render_template, request, redirect, url_for, session, flash, current_app)
from datetime import datetime
import os
from routes.auth_routes import role_required
from models.project_model import ProjectModel
from models.feedback_model import FeedbackModel
from models.user_model import UserModel

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

# REMOVED the broken module-level: project = ProjectModel.get_by_id(...)


@teacher_bp.route('/dashboard')
@role_required('teacher')
def dashboard():
    total_projects = ProjectModel.count_all()
    pending        = ProjectModel.count_by_status('pending')
    reviewed       = ProjectModel.count_by_status('reviewed')
    return render_template('teacher/dashboard.html',
                           username=session.get('username'),
                           total_projects=total_projects,
                           pending=pending,
                           reviewed=reviewed)


@teacher_bp.route('/projects')
@role_required('teacher')
def project_list():
    tech_filter       = request.args.get('tech_stack', '').strip()
    innovation_filter = request.args.get('innovation_level', '').strip()
    status_filter     = request.args.get('status', '').strip()

    filters = {}
    if tech_filter:       filters['tech_stack'] = tech_filter
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


@teacher_bp.route('/projects/<project_id>')
@role_required('teacher')
def project_detail(project_id):
    project = ProjectModel.get_by_id(project_id)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('teacher.project_list'))

    student           = UserModel.find_by_id(str(project['student_id']))
    existing_feedback = FeedbackModel.get_for_project(project_id)

    return render_template('teacher/project_detail.html',
                           project=project,
                           student=student,
                           existing_feedback=existing_feedback,
                           username=session.get('username'))


@teacher_bp.route('/download/<project_id>')
@role_required('teacher')
def download_file(project_id):
    """
    Fetch the project by ID, then redirect to its Cloudinary URL.
    project_id passed in URL instead of filename — no local disk needed.
    """
    project = ProjectModel.get_by_id(project_id)
    if not project or not project.get('file_path'):
        flash('File not found.', 'error')
        return redirect(url_for('teacher.project_list'))
    return redirect(project['file_path'])


@teacher_bp.route('/projects/<project_id>/feedback', methods=['GET', 'POST'])
@role_required('teacher')
def give_feedback(project_id):
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

        try:
            quality_rating = int(quality_rating)
            if quality_rating < 1 or quality_rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            quality_rating = None

        if existing_feedback:
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
            FeedbackModel.create_feedback(
                project_id=project_id,
                teacher_id=session['user_id'],
                student_id=str(project['student_id']),
                remarks=remarks,
                suggestions=suggestions,
                improvement_notes=improvement_notes
            )
            ProjectModel.update_status(project_id, 'reviewed')
            if quality_rating:
                ProjectModel.update_quality_rating(project_id, quality_rating)
            flash('Feedback submitted successfully!', 'success')

        return redirect(url_for('teacher.project_detail', project_id=project_id))

    return render_template('teacher/give_feedback.html',
                           project=project,
                           existing_feedback=existing_feedback,
                           username=session.get('username'))