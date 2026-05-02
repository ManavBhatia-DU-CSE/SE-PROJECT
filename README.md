# FnB – Fetch and Build

### Student Project Review and Feedback Platform

**Implementation version:** 2.0  
**Specification:** [SRS V2 Final Doc.pdf](SRS%20V2%20Final%20Doc.pdf) — *Software Requirements Specification and Design for FnB (Fetch and Build), Version 2.0* (IEEE 830-1998)

This repository implements the system described in that document. Feature scope, requirements IDs (`REQ-4.x.x`), design artifacts (`D-CL-xx`, `D-DB-xx`, `D-SQ-xx`, `D-SEC-xx`, `D-ARCH-xx`), and traceability (SRS Section 6) follow the SRS unless noted under [Implementation notes](#implementation-notes-vs-srs).

---

## Specification summary (from SRS V2)

| SRS | Content |
|-----|--------|
| §1 | Introduction — purpose, scope, objectives (product replaces informal review with a centralized platform). |
| §2 | Overall description — standalone web app; users: Student, Teacher, Admin; stack per SRS: HTML/CSS/JS, Flask, MongoDB. |
| §3 | External interfaces — web UI, HTTP/HTTPS, MongoDB, Chrome as reference browser. |
| §4 | System features — REQ-4.1.x (auth), REQ-4.2.x (projects), REQ-4.3.x (feedback). |
| §5 | Software design — three-tier architecture (§5.1), class/sequence diagrams (§5.2), MongoDB schema (§5.3), security design (§5.4). |
| §6 | Traceability — requirement-to-design mapping. |
| §7 | Nonfunctional requirements — performance, safety, security, quality attributes; Business Rules 1–7 (§7.5). |
| §8 + Appendices | Other requirements, glossary, TBD list. |

**SRS revision history (document):** 2026-01-24 initial → 2026-01-26 IEEE alignment → 2026-02-23 **Version 2.0** (design §5 + traceability §6).

---

## Team members and contributions

| Member | Role | Contribution |
|--------|------|--------------|
| **Shashi** | Backend lead | `app.py`, `routes/auth_routes.py`, `routes/student_routes.py`, `routes/teacher_routes.py`, `routes/admin_routes.py` |
| **Manav** | Database lead | `db.py`, `models/user_model.py`, `models/project_model.py`, `models/feedback_model.py` |
| **Harsh** | Frontend base & documentation | Core Jinja templates (`templates/base.html`, `templates/login.html`, `templates/register.html`, `templates/change_password.html`, landing integration); **maintains this README** aligned with **SRS V2 Final Doc.pdf** |
| **Hitesh** | CSS + student UI | `static/css/style.css`, `templates/student/dashboard.html`, `templates/student/submit_project.html`, `templates/student/my_feedback.html` |
| **Abhishek** | Teacher + admin UI | `templates/teacher/*.html`, `templates/admin/*.html` |

---

## Project overview (SRS §1.4, §2.2)

FnB digitizes student project evaluation: students submit work and metadata; teachers review, filter, and record structured feedback; administrators manage accounts. The **presentation layer** uses a **React** landing experience (`FnB_ProjectManagement.jsx`, CDN) plus **Jinja2** templates for authenticated flows, served by **Flask** (SRS §5.1). Persistent data lives in **MongoDB** (collections `users`, `projects`, `feedback` per SRS §5.3).

### Key features (mapped to SRS §4)

- **REQ-4.1.x** — Registration, login, roles, password change, admin user management, logout  
- **REQ-4.2.x** — Project submission (with optional file upload), association to student, teacher list/detail, feedback entry, filtering (tech, innovation, status; quality via rating; USP in data model), student-only feedback views  
- **REQ-4.3.x** — Feedback stored and linked to project and student; updates with `updated_at` (overwrite model per SRS §5.3 / TBD-4)

---

## Architecture (SRS §5.1 – three-tier)

```
[Browser – HTML/CSS/JS + React landing]     ← Presentation layer
  ├── Landing / demo (React)                  FnB_ProjectManagement.jsx
  └── Authenticated pages (Jinja2)           templates/**/*.html
        │
        │ HTTP / HTTPS (HTTPS in production per SRS §3.4, §5.4.2 D-SEC-01)
        ▼
[Flask – Python]                             ← Application logic layer
  ├── Auth (REQ-4.1.x)      ├── Project (REQ-4.2.x)
  ├── Feedback (REQ-4.3.x)  └── Admin (REQ-4.1.5)
        │
        │ PyMongo
        ▼
[MongoDB]                                    ← Data layer
  ├── users      (D-DB-01)
  ├── projects   (D-DB-02)
  └── feedback   (D-DB-03)
```

---

## Repository structure

```
SE-PROJECT/
├── SRS V2 Final Doc.pdf        # Authoritative SRS & design (IEEE 830-1998, v2.0)
├── app.py                      # Flask entry (SRS §5.1 application layer)
├── db.py                       # PyMongo + index setup (supports NFR-01 / indexed queries)
├── requirements.txt
├── .env.example
├── .gitignore
├── FnB_ProjectManagement.jsx   # React landing assets (SRS presentation layer)
│
├── models/                     # Data layer accessors (D-CL-01 … D-CL-03)
│   ├── user_model.py
│   ├── project_model.py
│   └── feedback_model.py
│
├── routes/                     # Blueprints / RBAC (D-CL-04 patterns)
│   ├── auth_routes.py
│   ├── student_routes.py
│   ├── teacher_routes.py
│   └── admin_routes.py
│
├── templates/                  # Jinja2 UI (SRS §3.1)
│   ├── base.html, login.html, register.html, change_password.html
│   ├── student/
│   ├── teacher/
│   └── admin/
│
└── static/
    ├── css/style.css
    └── user_manual.html
```

---

## Setup and run

### Prerequisites (SRS §2.4, §2.5)

- Python 3.9+  
- MongoDB reachable at your `MONGO_URI` (local or Atlas)  
- Modern browser (Chrome per SRS)  
- Optional: [Cloudinary](https://cloudinary.com/) account for student file uploads (see below)

### 1. Clone

```bash
git clone https://github.com/ManavBhatia-DU-CSE/SE-PROJECT.git
cd SE-PROJECT
```

### 2. Virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Copy `.env.example` to `.env` and set:

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Flask session signing (SRS §5.4.1, D-SEC-03) |
| `MONGO_URI` | MongoDB connection string |
| `CLOUDINARY_*` | File uploads from student submit flow |

### 5. Run the application

Ensure MongoDB is available, then:

```bash
python app.py
```

On Windows, if `python` is not the venv interpreter:

```bash
venv\Scripts\python.exe app.py
```

Open **http://127.0.0.1:5000** — use the landing page entry point, then **Sign in** for the Flask app.

---

## First-time admin (SRS REQ-4.1.5)

Admin accounts are not self-registered. Seed one user in `users` (example: `mongo` shell or a short script). Example using the app context:

```python
from app import app
from db import mongo
import bcrypt
from datetime import datetime, timezone

with app.app_context():
    password_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt(rounds=10))
    mongo.db.users.insert_one({
        "username": "admin",
        "password_hash": password_hash,
        "role": "admin",
        "email": "admin@fnb.com",
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
    })
    print("Admin created: admin / admin123")
```

---

## Security measures (SRS §5.4.2)

| ID | Measure | Implementation |
|----|---------|----------------|
| D-SEC-01 | HTTPS | TLS / redirect in production |
| D-SEC-02 | Password hashing | bcrypt (≥10 rounds) |
| D-SEC-03 | Session security | Flask signed sessions; cleared on logout |
| D-SEC-04 | RBAC | `login_required` / `role_required` on routes |
| D-SEC-05 | Input validation | Server-side checks on forms |
| D-SEC-06 | CSRF | *SRS lists Flask-WTF-style CSRF; not yet wired in this repo — treat as hardening backlog.* |
| D-SEC-07 | Data isolation | Student queries scoped by `student_id` / session |
| D-SEC-08 | File uploads | Extension allow-list, size limit, sanitized names; files sent to Cloudinary, URL stored in `file_path` |
| D-SEC-09 / D-SEC-10 | DB privileges / backup | Operational concerns per deployment (SRS TBD-1) |

---

## SRS functional requirements coverage

| REQ ID | Feature (abbrev.) | Status |
|--------|-------------------|--------|
| REQ-4.1.1 | Registration, unique username | Implemented |
| REQ-4.1.2 | Secure login | Implemented |
| REQ-4.1.3 | Roles Student / Teacher / Admin | Implemented |
| REQ-4.1.4 | Change password when authenticated | Implemented |
| REQ-4.1.5 | Admin manage users | Implemented |
| REQ-4.1.6 | Logout | Implemented |
| REQ-4.2.1 | Submit project + optional file | Implemented |
| REQ-4.2.2 | Project linked to student | Implemented |
| REQ-4.2.3 | Teacher list / detail | Implemented |
| REQ-4.2.4 | Feedback, suggestions, remarks | Implemented |
| REQ-4.2.5 | Filter by tech, innovation, status; quality rating | Implemented (USP stored; filter UI focuses on tech / innovation / status) |
| REQ-4.2.6 | Student sees only own feedback | Implemented |
| REQ-4.3.1 | Feedback linked to project + student | Implemented |
| REQ-4.3.2 | Enforce student-only feedback access | Implemented |
| REQ-4.3.3 | Teacher updates feedback | Implemented |

---

## Implementation notes vs SRS

- **File storage (D-DB-02 `file_path`):** SRS describes a server-side path; this codebase stores a **Cloudinary secure URL** after upload. Behavior still satisfies secure upload (D-SEC-08) with cloud delivery instead of local disk.  
- **CSRF (D-SEC-06):** Listed in SRS §5.4.2; forms here do not yet include CSRF tokens — align with SRS in a future change if required for your evaluation.  
- **Indexes:** Created at startup in `db.py` (see SRS NFR-01 / indexed fields in §5.3) to support typical query paths.

---

## Technologies

- **Backend:** Python, Flask 3.x  
- **Database:** MongoDB, Flask-PyMongo / PyMongo  
- **Security:** bcrypt, Flask sessions  
- **Frontend:** HTML5, CSS3, JavaScript; React (landing) via CDN; Jinja2 templates  
- **Media:** Cloudinary (optional but recommended for uploads)

---

## References

- **Primary:** [SRS V2 Final Doc.pdf](SRS%20V2%20Final%20Doc.pdf)  
- IEEE 830-1998 — Software Requirements Specifications  
- [Flask](https://flask.palletsprojects.com/), [MongoDB](https://www.mongodb.com/docs/) (per SRS §1.5)

---

*FnB (Fetch and Build) — implementation aligned with **SRS V2 Final Doc.pdf**. README maintained by **Harsh** (documentation + base templates); full team credits in table above.*

---

## React UI prototype

`FnB_ProjectManagement.jsx` is a standalone React prototype that was used only to visualize the initial look and flow of the FnB application. It is not connected to the Flask routes, MongoDB models, templates, deployment pipeline, or production runtime.

No changes are required in the JSX file for the Flask application to run. To preview it locally as a demo, run it in a separate Vite React shell:

```powershell
npm create vite@latest fnb-prototype-demo -- --template react
cd fnb-prototype-demo
npm install
Copy-Item ..\FnB_ProjectManagement.jsx .\src\App.jsx
npm run dev
```

Then open the local URL printed by Vite, usually `http://localhost:5173/`.
