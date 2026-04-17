# FnB – Fetch and Build
### Student Project Review and Feedback Platform
**Version:** 2.0 | **SRS Standard:** IEEE 830-1998

---

## Team Members & Contributions

| Member | Role | Contribution |
|---|---|---|
| **Shashi** | Backend Lead | `app.py`, `routes/auth_routes.py`, `routes/student_routes.py`, `routes/teacher_routes.py`, `routes/admin_routes.py` |
| **Manav** | Database Lead | `models/db.py`, `models/user_model.py`, `models/project_model.py`, `models/feedback_model.py` |
| **Harsh** | HTML Templates & Landing | `templates/base.html`, `templates/login.html`, `templates/register.html`, `templates/change_password.html`, `templates/landing.html` |
| **Hitesh** | CSS + Student UI | `static/css/style.css`, `templates/student/dashboard.html`, `templates/student/submit_project.html`, `templates/student/my_feedback.html` |
| **Abhishek** | Teacher + Admin UI | `templates/teacher/dashboard.html`, `templates/teacher/project_list.html`, `templates/teacher/project_detail.html`, `templates/teacher/give_feedback.html`, `templates/admin/dashboard.html`, `templates/admin/manage_users.html` |

---

## Project Overview

FnB is a web-based platform that digitizes the student project evaluation process. Teachers can review student projects and provide structured feedback; students can securely access their personalized feedback.

The landing page (`/`) is built with **React** (loaded via CDN), providing an interactive demo and gateway to the platform. All authenticated pages (dashboards, project submission, feedback, admin) are served as Flask/Jinja2 templates.

### Key Features
- **React landing page** with interactive demo for all three roles
- Role-based authentication (Student, Teacher, Admin)
- Project submission with file upload
- Filtering projects by tech stack, innovation level, status
- Structured feedback (remarks, suggestions, improvement notes)
- Admin user management (create, enable/disable, assign roles)
- bcrypt password hashing, Flask session security, RBAC

---

## Architecture (SRS Section 5.1 – Three-Tier)

```
[Browser – React + HTML/CSS/JS]  ← Presentation Layer
  ├── Landing Page (React)            FnB_ProjectManagement.jsx
  └── App Pages (Jinja2 Templates)    templates/**/*.html
        |
        | HTTP Requests
        ↓
[Flask Backend – Python]         ← Application Logic Layer
  ├── Auth Module    (REQ-4.1.x)
  ├── Project Module (REQ-4.2.x)
  ├── Feedback Module(REQ-4.3.x)
  └── Admin Module   (REQ-4.1.5)
        |
        | PyMongo Driver
        ↓
[MongoDB – 3 Collections]        ← Data Layer
  ├── users
  ├── projects
  └── feedback
```

---

---

## Project Structure

```
SE-PROJECT/
├── app.py                      # Shashi – Flask app entry point
├── db.py                       # Manav  – PyMongo initialization
├── requirements.txt            # Python dependencies
├── .gitignore
│
├── models/                     # Manav – MongoDB models (D-CL-01 to D-CL-03)
│   ├── user_model.py           #   users collection
│   ├── project_model.py        #   projects collection
│   └── feedback_model.py       #   feedback collection
│
├── routes/                     # Shashi – Flask Blueprints
│   ├── auth_routes.py          #   /login, /register, /logout, /change-password
│   ├── student_routes.py       #   /student/*
│   ├── teacher_routes.py       #   /teacher/*
│   └── admin_routes.py         #   /admin/*
│
├── templates/                  # Harsh + Hitesh + Abhishek – Jinja2 HTML
│   ├── base.html               # Harsh  – Base layout + navbar + flash
│   ├── login.html              # Harsh  – Login page
│   ├── register.html           # Harsh  – Registration page
│   ├── change_password.html    # Harsh  – Change password
│   ├── student/
│   │   ├── dashboard.html      # Hitesh – Student home
│   │   ├── submit_project.html # Hitesh – Project submission form
│   │   └── my_feedback.html    # Hitesh – Student feedback view
│   ├── teacher/
│   │   ├── dashboard.html      # Abhishek – Teacher home
│   │   ├── project_list.html   # Abhishek – Projects table + filters
│   │   ├── project_detail.html # Abhishek – Single project detail
│   │   └── give_feedback.html  # Abhishek – Feedback form
│   └── admin/
│       ├── dashboard.html      # Abhishek – Admin home + stats
│       └── manage_users.html   # Abhishek – User management
│
├── static/
│   └── css/
│       └── style.css           # Hitesh – Complete stylesheet
│
└── uploads/                    # Secure file storage (D-SEC-08)
```

---

##  Setup & Run Instructions

### 1. Prerequisites
- Python 3.9+
- MongoDB running locally on port 27017
- Git

### 2. Clone the repository
```bash
git clone https://github.com/ManavBhatia-DU-CSE/SE-PROJECT
cd SE-PROJECT
```

### 3. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Start MongoDB
```bash
# Make sure MongoDB is running
mongod
```

### 6. Run the application
```bash
python app.py
```

### 7. Open in browser
```
http://localhost:5000
```

---

## First-Time Setup (Create Admin Account)

Since admin accounts can only be created by another admin, you need to seed one manually. Run this in a Python shell:

```python
from app import app
from db import mongo
import bcrypt
from datetime import datetime

with app.app_context():
    password_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt(rounds=10))
    mongo.db.users.insert_one({
        'username': 'admin',
        'password_hash': password_hash,
        'role': 'admin',
        'email': 'admin@fnb.com',
        'is_active': True,
        'created_at': datetime.utcnow()
    })
    print("Admin created! Login: admin / admin123")
```

---

## Test Credentials (after seeding)

| Role | Username | Password |
|---|---|---|
| Admin | admin | admin123 |
| Student | (register via /register) | — |
| Teacher | (register via /register or admin creates) | — |

---

## Security Features (SRS Section 5.4)

| ID | Measure | Implementation |
|---|---|---|
| D-SEC-01 | HTTPS | TLS in production |
| D-SEC-02 | Password Hashing | bcrypt (10 rounds) |
| D-SEC-03 | Session Security | HMAC-SHA256 signed Flask sessions |
| D-SEC-04 | RBAC | `role_required()` decorator on all routes |
| D-SEC-05 | Input Validation | Server-side validation on all forms |
| D-SEC-07 | Data Isolation | `student_id` filter in all student DB queries |
| D-SEC-08 | File Upload Security | `werkzeug.secure_filename`, extension whitelist |

---

## SRS Requirement Coverage

| REQ ID | Feature | Status |
|---|---|---|
| REQ-4.1.1 | User registration with unique username
| REQ-4.1.2 | Secure login with credentials 
| REQ-4.1.3 | Role assignment and enforcement
| REQ-4.1.4 | Authenticated password change 
| REQ-4.1.5 | Admin user account management
| REQ-4.1.6 | Logout at any time 
| REQ-4.2.1 | Student project submission with file
| REQ-4.2.2 | Project associated with student account
| REQ-4.2.3 | Teacher views submitted projects
| REQ-4.2.4 | Teacher provides feedback/suggestions/remarks 
| REQ-4.2.5 | Filter projects by quality/innovation/tech/USP
| REQ-4.2.6 | Student views only own feedback
| REQ-4.3.1 | Feedback stored securely with project+student
| REQ-4.3.2 | Students access only their own feedback
| REQ-4.3.3 | Teacher can update existing feedback

---

## Technologies Used

- **Backend:** Python, Flask 3.0
- **Database:** MongoDB, Flask-PyMongo
- **Security:** bcrypt, Flask sessions
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **IDE:** Visual Studio Code
- **Browser:** Google Chrome

---

*FnB – Fetch and Build | Student Project Review and Feedback Platform | Version 2.0*
*SRS Reference: IEEE 830-1998*1:5000** to see the React landing page.
Click **"Sign in to your account"** to use the real Flask application.
