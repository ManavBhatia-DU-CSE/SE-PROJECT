# FnB – Fetch and Build
### Student Project Review and Feedback Platform
**Version:** 2.0 | **SRS Standard:** IEEE 830-1998

---

## Team Members & Contributions

| Member | Role | Contribution |
|---|---|---|
| **Shashi** | Backend Lead | `app.py`, `routes/auth_routes.py`, `routes/student_routes.py`, `routes/teacher_routes.py`, `routes/admin_routes.py` |
| **Manav** | Database Lead | `db.py`, `models/user_model.py`, `models/project_model.py`, `models/feedback_model.py` |
| **Harsh** | HTML Templates | `templates/base.html`, `templates/login.html`, `templates/register.html`, `templates/change_password.html` |
| **Hitesh** | CSS + Student UI | `static/css/style.css`, `templates/student/dashboard.html`, `templates/student/submit_project.html`, `templates/student/my_feedback.html` |
| **Abhishek** | Teacher + Admin UI | `templates/teacher/dashboard.html`, `templates/teacher/project_list.html`, `templates/teacher/project_detail.html`, `templates/teacher/give_feedback.html`, `templates/admin/dashboard.html`, `templates/admin/manage_users.html` |

---

## Project Overview

FnB is a web-based platform that digitizes the student project evaluation process. Teachers can review student projects and provide structured feedback; students can securely access their personalized feedback.

### Key Features
- Role-based authentication (Student, Teacher, Admin)
- Project submission with file upload
- Filtering projects by tech stack, innovation level, status
- Structured feedback (remarks, suggestions, improvement notes)
- Admin user management (create, enable/disable, assign roles)
- bcrypt password hashing, Flask session security, RBAC

---

## Architecture (SRS Section 5.1 – Three-Tier)

```
[Browser – HTML/CSS/JS]          ← Presentation Layer
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