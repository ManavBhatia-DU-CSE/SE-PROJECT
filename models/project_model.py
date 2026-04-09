"""
FnB - Project Model (MongoDB projects collection)
Author: Manav
SRS Reference: Section 5.3 - Collection 2: projects
D-DB-02: projects collection schema
D-CL-02: Project class attributes and methods
REQ-4.2.1, REQ-4.2.2, REQ-4.2.3, REQ-4.2.5

Collection Schema:
  _id              : ObjectId  (auto)
  student_id       : ObjectId  (ref: users, indexed)
  title            : String
  description      : String
  tech_stack       : String    (indexed, used for filtering)
  usp              : String
  innovation_level : String    (low|medium|high, indexed)
  quality_rating   : Integer   (1-5, set by teacher)
  file_path        : String    (server-side path, D-SEC-08)
  status           : String    (pending|reviewed, indexed)
  submitted_at     : DateTime  (indexed)

Indexes: student_id, status, tech_stack, innovation_level
"""

from datetime import datetime
from bson import ObjectId
from db import mongo


class ProjectModel:
    """
    Handles all MongoDB operations on the 'projects' collection.
    Implements Project class methods from D-CL-02.
    """

    COLLECTION = 'projects'

    # ── Create ────────────────────────────────────────────────────────────────

    @staticmethod
    def create_project(student_id, title, description,
                       tech_stack, usp, innovation_level, file_path=None):
        """
        submit() : Boolean – Insert new project document.
        REQ-4.2.1: Students submit projects online.
        REQ-4.2.2: System associates project with student_id.
        D-DB-02 schema enforced here.
        """
        project_doc = {
            'student_id':       ObjectId(student_id),   # Foreign key → users
            'title':            title,
            'description':      description,
            'tech_stack':       tech_stack,
            'usp':              usp,
            'innovation_level': innovation_level,        # 'low'|'medium'|'high'
            'quality_rating':   None,                   # Set by teacher later
            'file_path':        file_path,
            'status':           'pending',              # Default status
            'submitted_at':     datetime.utcnow()
        }
        return mongo.db[ProjectModel.COLLECTION].insert_one(project_doc)

    # ── Read ─────────────────────────────────────────────────────────────────

    @staticmethod
    def get_by_student(student_id):
        """
        D-SEC-07: Data isolation – only projects where student_id == session.user_id.
        REQ-4.2.2: Projects associated with specific student.
        Returns list sorted by submitted_at descending.
        """
        return list(
            mongo.db[ProjectModel.COLLECTION]
            .find({'student_id': ObjectId(student_id)})
            .sort('submitted_at', -1)
        )

    @staticmethod
    def get_by_id(project_id):
        """
        getDetails() : Project – Fetch single project by ObjectId.
        REQ-4.2.3: Teachers view project details.
        """
        try:
            return mongo.db[ProjectModel.COLLECTION].find_one(
                {'_id': ObjectId(project_id)}
            )
        except Exception:
            return None

    @staticmethod
    def get_all_filtered(filters=None):
        """
        filterByQuality() / filterByTech() / filterByUSP() / filterByInnovation()
        REQ-4.2.5: Teachers filter by quality, innovation, tech_stack, USP.
        D-CL-02: filter methods. D-DB-02: uses indexed fields.
        """
        query = {}
        if filters:
            if 'tech_stack' in filters and filters['tech_stack']:
                # Case-insensitive partial match
                query['tech_stack'] = {
                    '$regex': filters['tech_stack'], '$options': 'i'
                }
            if 'innovation_level' in filters and filters['innovation_level']:
                query['innovation_level'] = filters['innovation_level']
            if 'status' in filters and filters['status']:
                query['status'] = filters['status']

        return list(
            mongo.db[ProjectModel.COLLECTION]
            .find(query)
            .sort('submitted_at', -1)
        )

    # ── Count helpers for dashboards ──────────────────────────────────────────

    @staticmethod
    def count_all():
        """Total project count."""
        return mongo.db[ProjectModel.COLLECTION].count_documents({})

    @staticmethod
    def count_by_status(status):
        """Count projects by status (pending/reviewed)."""
        return mongo.db[ProjectModel.COLLECTION].count_documents({'status': status})

    # ── Update ────────────────────────────────────────────────────────────────

    @staticmethod
    def update_status(project_id, status):
        """
        Update project status to 'reviewed' after feedback is given.
        D-SQ-03: update Project.status=reviewed
        """
        return mongo.db[ProjectModel.COLLECTION].update_one(
            {'_id': ObjectId(project_id)},
            {'$set': {'status': status}}
        )

    @staticmethod
    def update_quality_rating(project_id, rating):
        """
        Teacher assigns quality rating (1-5) to a project.
        REQ-4.2.5: quality used as filter criterion.
        D-DB-02: quality_rating field.
        """
        return mongo.db[ProjectModel.COLLECTION].update_one(
            {'_id': ObjectId(project_id)},
            {'$set': {'quality_rating': int(rating)}}
        )
