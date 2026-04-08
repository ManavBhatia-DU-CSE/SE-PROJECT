"""
FnB - Admin Routes Module
Author: Shashi
SRS Reference: Section 4.1.5 - Admin User Account Management
REQ-4.1.5: Create, disable, assign roles
D-SQ-05: Admin Manages User Accounts
D-CL-01: Admin.manageUsers(), Admin.disableUser(), Admin.assignRole()
"""

import bcrypt
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash)
from routes.auth_routes import role_required
from models.user_model import UserModel
from models.project_model import ProjectModel
from models.feedback_model import FeedbackModel

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# ─── Admin Dashboard ──────────────────────────────────────────────────────────

@admin_bp.route('/dashboard')
@role_required('admin')
def dashboard():
    """Admin home with system-wide stats. REQ-4.1.5"""
    total_users     = UserModel.count_all()
    total_students  = UserModel.count_by_role('student')
    total_teachers  = UserModel.count_by_role('teacher')
    total_projects  = ProjectModel.count_all()
    total_feedback  = FeedbackModel.count_all()
    return render_template('admin/dashboard.html',
                           username=session.get('username'),
                           total_users=total_users,
                           total_students=total_students,
                           total_teachers=total_teachers,
                           total_projects=total_projects,
                           total_feedback=total_feedback)


# ─── Manage Users ─────────────────────────────────────────────────────────────

@admin_bp.route('/users')
@role_required('admin')
def manage_users():
    """
    List all users for admin management.
    D-SQ-05: enforceRole(Admin) → fetchAll users → user management panel
    REQ-4.1.5
    """
    users = UserModel.get_all()
    return render_template('admin/manage_users.html',
                           users=users,
                           username=session.get('username'))


# ─── Create User (Admin) ──────────────────────────────────────────────────────

@admin_bp.route('/users/create', methods=['POST'])
@role_required('admin')
def create_user():
    """
    Admin creates a new user account directly.
    REQ-4.1.5, D-SQ-05: POST create user → User.update() → update doc
    """
    username  = request.form.get('username', '').strip()
    email     = request.form.get('email', '').strip()
    password  = request.form.get('password', '').strip()
    role      = request.form.get('role', 'student')

    if not username or not email or not password:
        flash('All fields are required to create a user.', 'error')
        return redirect(url_for('admin.manage_users'))

    if role not in ['student', 'teacher', 'admin']:
        flash('Invalid role selected.', 'error')
        return redirect(url_for('admin.manage_users'))

    if UserModel.find_by_username(username):
        flash(f'Username "{username}" already exists.', 'error')
        return redirect(url_for('admin.manage_users'))

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=10))
    UserModel.create_user(username, password_hash, role, email)
    flash(f'User "{username}" created successfully as {role}.', 'success')
    return redirect(url_for('admin.manage_users'))


# ─── Toggle User Active/Disable ───────────────────────────────────────────────

@admin_bp.route('/users/<user_id>/toggle', methods=['POST'])
@role_required('admin')
def toggle_user(user_id):
    """
    Enable or disable a user account. REQ-4.1.5
    D-SQ-05: User.update(is_active=False) → update doc → success confirmation
    Prevents admin from disabling their own account.
    """
    if user_id == session['user_id']:
        flash('You cannot disable your own account.', 'error')
        return redirect(url_for('admin.manage_users'))

    user = UserModel.find_by_id(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('admin.manage_users'))

    new_status = not user.get('is_active', True)
    UserModel.set_active_status(user_id, new_status)
    status_text = 'enabled' if new_status else 'disabled'
    flash(f'User "{user["username"]}" has been {status_text}.', 'success')
    return redirect(url_for('admin.manage_users'))


# ─── Change User Role ─────────────────────────────────────────────────────────

@admin_bp.route('/users/<user_id>/role', methods=['POST'])
@role_required('admin')
def change_role(user_id):
    """
    Admin assigns a new role to a user. REQ-4.1.5, Admin.assignRole()
    """
    if user_id == session['user_id']:
        flash('You cannot change your own role.', 'error')
        return redirect(url_for('admin.manage_users'))

    new_role = request.form.get('role', '').strip()
    if new_role not in ['student', 'teacher', 'admin']:
        flash('Invalid role.', 'error')
        return redirect(url_for('admin.manage_users'))

    user = UserModel.find_by_id(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('admin.manage_users'))

    UserModel.update_role(user_id, new_role)
    flash(f'Role for "{user["username"]}" updated to {new_role}.', 'success')
    return redirect(url_for('admin.manage_users'))
