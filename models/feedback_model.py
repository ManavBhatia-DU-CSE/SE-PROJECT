"""
FnB - Feedback Model (MongoDB feedback collection)
Author: Manav
SRS Reference: Section 5.3 - Collection 3: feedback
D-DB-03: feedback collection schema
D-CL-03: Feedback class attributes and methods
REQ-4.3.1, REQ-4.3.2, REQ-4.3.3

Collection Schema:
  _id               : ObjectId  (auto)
  project_id        : ObjectId  (ref: projects, UNIQUE – one review per project)
  teacher_id        : ObjectId  (ref: users, indexed)
  student_id        : ObjectId  (ref: users, indexed – enables direct student query)
  remarks           : String    (required)
  suggestions       : String
  improvement_notes : String
  created_at        : DateTime
  updated_at        : DateTime  (null if never updated – TBD-4 resolved as overwrite)

Indexes: project_id (unique), student_id, teacher_id
"""

from datetime import datetime
from bson import ObjectId
from db import mongo


class FeedbackModel:
    """
    Handles all MongoDB operations on the 'feedback' collection.
    Implements Feedback class methods from D-CL-03.
    """

    COLLECTION = 'feedback'

    # ── Create ────────────────────────────────────────────────────────────────

    @staticmethod
    def create_feedback(project_id, teacher_id, student_id,
                        remarks, suggestions='', improvement_notes=''):
        """
        save() : Boolean – Insert new feedback document.
        REQ-4.3.1: Store teacher feedback securely, associated with project + student.
        D-DB-03 schema. One feedback per project (project_id is unique index).
        """
        feedback_doc = {
            'project_id':        ObjectId(project_id),   # FK → projects (unique)
            'teacher_id':        ObjectId(teacher_id),   # FK → users (teacher)
            'student_id':        ObjectId(student_id),   # FK → users (student)
            'remarks':           remarks,
            'suggestions':       suggestions,
            'improvement_notes': improvement_notes,
            'created_at':        datetime.utcnow(),
            'updated_at':        None                    # Null until first update
        }
        return mongo.db[FeedbackModel.COLLECTION].insert_one(feedback_doc)

    # ── Read ─────────────────────────────────────────────────────────────────

    @staticmethod
    def get_for_student(student_id):
        """
        getForStudent(id) : List – Retrieve all feedback for a student.
        REQ-4.3.2, D-SQ-04: find(student_id) – Data isolation enforced here.
        D-SEC-07: student_id filter from authenticated session.
        Only feedback where student_id == session.user_id is returned.
        """
        pipeline = [
            {'$match': {'student_id': ObjectId(student_id)}},
            # Join with projects collection to get project title
            {'$lookup': {
                'from': 'projects',
                'localField': 'project_id',
                'foreignField': '_id',
                'as': 'project'
            }},
            {'$unwind': {'path': '$project', 'preserveNullAndEmptyArrays': True}},
            # Join with users to get teacher name
            {'$lookup': {
                'from': 'users',
                'localField': 'teacher_id',
                'foreignField': '_id',
                'as': 'teacher'
            }},
            {'$unwind': {'path': '$teacher', 'preserveNullAndEmptyArrays': True}},
            {'$sort': {'created_at': -1}}
        ]
        return list(mongo.db[FeedbackModel.COLLECTION].aggregate(pipeline))

    @staticmethod
    def get_for_project(project_id):
        """
        getForProject(id) : Feedback – Get feedback for a specific project.
        REQ-4.3.3: Teachers view/update existing feedback.
        Returns single document (one review per project).
        """
        try:
            return mongo.db[FeedbackModel.COLLECTION].find_one(
                {'project_id': ObjectId(project_id)}
            )
        except Exception:
            return None

    # ── Count helpers ─────────────────────────────────────────────────────────

    @staticmethod
    def count_all():
        """Total feedback entries for admin dashboard."""
        return mongo.db[FeedbackModel.COLLECTION].count_documents({})

    # ── Update ────────────────────────────────────────────────────────────────

    @staticmethod
    def update_feedback(feedback_id, remarks, suggestions='', improvement_notes=''):
        """
        update() : Boolean – Overwrite existing feedback (TBD-4 resolved as overwrite).
        REQ-4.3.3: Teachers can update feedback when required.
        D-DB-03: updated_at timestamp set on update.
        """
        return mongo.db[FeedbackModel.COLLECTION].update_one(
            {'_id': ObjectId(feedback_id)},
            {'$set': {
                'remarks':           remarks,
                'suggestions':       suggestions,
                'improvement_notes': improvement_notes,
                'updated_at':        datetime.utcnow()   # D-DB-03: updated_at
            }}
        )
