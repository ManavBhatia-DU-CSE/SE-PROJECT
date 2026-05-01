"""
FnB - Database Connection Module
Author: Manav
SRS Reference: Section 5.3 - Database Schema, Section 2.1 - MongoDB (Data Layer)
D-DB-01: users collection
D-DB-02: projects collection
D-DB-03: feedback collection
D-SEC-09: MongoDB dedicated app user with minimum privileges
D-ARCH-01: Data Layer (MongoDB Database)
"""

import warnings

from flask_pymongo import PyMongo
from pymongo.errors import PyMongoError

# Single PyMongo instance shared across all models
mongo = PyMongo()


def ensure_indexes():
    """
    Idempotent index setup for query paths used in FnB.
    Call inside Flask app context after mongo.init_app().
    """
    try:
        db = mongo.db
        db.users.create_index('username', unique=True)
        db.users.create_index('role')

        db.projects.create_index([('student_id', 1), ('submitted_at', -1)])
        db.projects.create_index('status')
        db.projects.create_index('tech_stack')
        db.projects.create_index('innovation_level')

        db.feedback.create_index('project_id', unique=True)
        db.feedback.create_index('student_id')
        db.feedback.create_index('teacher_id')
    except PyMongoError as exc:
        warnings.warn(
            f'MongoDB indexes could not be created (is the server running?): {exc}',
            RuntimeWarning,
            stacklevel=2,
        )