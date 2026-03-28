# Author: Shashi
# SRS Reference: Section 4.1 - System Feature 1: User Authentication
# REQ-4.1.1 (Registration), REQ-4.1.2 (Login), REQ-4.1.3 (Roles),
# REQ-4.1.4 (Change Password), REQ-4.1.6 (Logout)
# D-SQ-01: User Login and Authentication Sequence Diagram
# D-SEC-02: Password Hashing (bcrypt), D-SEC-03: Session Security

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
import bcrypt
from models.user_model import UserModel

auth_bp = Blueprint('auth', __name__)


# ─── Decorators (AuthenticationManager – D-CL-04) ────────────────────────────

def login_required(f):
    """Ensures user is logged in. REQ-4.1.2"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    """Enforces RBAC – only allowed roles can access the route. REQ-4.1.3, D-SEC-04"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login to continue.', 'error')
                return redirect(url_for('auth.login'))
            if session.get('role') not in roles:
                flash('Access denied. You do not have permission for this page.', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated
    return decorator


# ─── Login Route ──────────────────────────────────────────────────────────────

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login. Verifies credentials, creates session.
    D-SQ-01: authenticate(u,p) → find(u) → verifyPwd() → createSession(user.role)
    REQ-4.1.2, D-SEC-02, D-SEC-03
    """
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Input validation – D-SEC-05
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')

        # Find user in DB (Manav's model)
        user = UserModel.find_by_username(username)

        # Verify password with bcrypt – D-SEC-02
        if user and user.get('is_active') and bcrypt.checkpw(
            password.encode('utf-8'), user['password_hash']
        ):
            # Create Flask session – D-SEC-03
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f"Welcome back, {user['username']}!", 'success')

            # Redirect based on role – REQ-4.1.3
            role_redirects = {
                'student': 'student.dashboard',
                'teacher': 'teacher.dashboard',
                'admin':   'admin.dashboard',
            }
            return redirect(url_for(role_redirects[user['role']]))
        else:
            # Generic error message (no username enumeration) – D-SEC-02
            flash('Invalid username or password, or account is disabled.', 'error')

    return render_template('login.html')


# ─── Register Route ───────────────────────────────────────────────────────────

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles new user registration with unique username.
    REQ-4.1.1, D-SEC-02 (password hashing), D-SEC-05 (input validation)
    """
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role     = request.form.get('role', 'student')

        # Server-side input validation – D-SEC-05
        errors = []
        if not username:
            errors.append('Username is required.')
        if not email or '@' not in email:
            errors.append('A valid email is required.')
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if role not in ['student', 'teacher']:
            role = 'student'

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('register.html')

        # Check uniqueness – REQ-4.1.1, Business Rule 2
        if UserModel.find_by_username(username):
            flash('Username already taken. Please choose another.', 'error')
            return render_template('register.html')

        # Hash password with bcrypt (10 rounds) – D-SEC-02
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=10))

        # Create user in MongoDB (Manav's model)
        UserModel.create_user(username, password_hash, role, email)

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# ─── Logout Route ─────────────────────────────────────────────────────────────

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Destroys session immediately. REQ-4.1.6, D-SEC-03 (destroySession())
    """
    username = session.get('username', 'User')
    session.clear()
    flash(f'{username} has been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))


# ─── Change Password Route ────────────────────────────────────────────────────

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Allows authenticated users to change their password.
    REQ-4.1.4, D-SEC-02 (bcrypt re-hash), User.changePassword()
    """
    if request.method == 'POST':
        current_pw  = request.form.get('current_password', '').strip()
        new_pw      = request.form.get('new_password', '').strip()
        confirm_pw  = request.form.get('confirm_password', '').strip()

        if not current_pw or not new_pw or not confirm_pw:
            flash('All fields are required.', 'error')
            return render_template('change_password.html')

        if new_pw != confirm_pw:
            flash('New passwords do not match.', 'error')
            return render_template('change_password.html')

        if len(new_pw) < 6:
            flash('New password must be at least 6 characters.', 'error')
            return render_template('change_password.html')

        # Verify current password
        user = UserModel.find_by_id(session['user_id'])
        if not user or not bcrypt.checkpw(current_pw.encode('utf-8'), user['password_hash']):
            flash('Current password is incorrect.', 'error')
            return render_template('change_password.html')

        # Hash and update new password
        new_hash = bcrypt.hashpw(new_pw.encode('utf-8'), bcrypt.gensalt(rounds=10))
        UserModel.update_password(session['user_id'], new_hash)

        flash('Password changed successfully!', 'success')

    return render_template('change_password.html')
