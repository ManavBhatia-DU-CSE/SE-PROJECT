"""
FnB - User Model (MongoDB users collection)
Author: Manav
SRS Reference: Section 5.3 - Collection 1: users
D-DB-01: users collection schema
D-CL-01: User class attributes and methods
REQ-4.1.1, REQ-4.1.2, REQ-4.1.3, REQ-4.1.4, REQ-4.1.5

Collection Schema:
  _id           : ObjectId  (auto)
  username      : String    (unique, indexed)
  password_hash : Binary    (bcrypt hash)
  role          : String    (enum: student|teacher|admin)
  email         : String
  is_active     : Boolean
  created_at    : DateTime
"""

from datetime import datetime
from bson import ObjectId
from db import mongo


class UserModel:
    """
    Handles all MongoDB operations on the 'users' collection.
    Implements User class methods from D-CL-01.
    """

    COLLECTION = 'users'

    # ── Create ────────────────────────────────────────────────────────────────

    @staticmethod
    def create_user(username, password_hash, role, email):
        """
        register() : Boolean – Insert a new user document.
        REQ-4.1.1: Unique username, REQ-4.1.3: role assignment
        D-DB-01 schema enforced here.
        """
        user_doc = {
            'username':      username,
            'password_hash': password_hash,
            'role':          role,          # 'student' | 'teacher' | 'admin'
            'email':         email,
            'is_active':     True,          # REQ-4.1.5: admin can disable
            'created_at':    datetime.utcnow()
        }
        return mongo.db[UserModel.COLLECTION].insert_one(user_doc)

    # ── Read ─────────────────────────────────────────────────────────────────

    @staticmethod
    def find_by_username(username):
        """Find user doc by unique username. REQ-4.1.1, REQ-4.1.2"""
        return mongo.db[UserModel.COLLECTION].find_one({'username': username})

    @staticmethod
    def find_by_id(user_id):
        """Find user doc by ObjectId string. Used in session lookups."""
        try:
            return mongo.db[UserModel.COLLECTION].find_one({'_id': ObjectId(user_id)})
        except Exception:
            return None

    @staticmethod
    def get_all():
        """
        Fetch all user documents. D-SQ-05: fetchAll users.
        REQ-4.1.5: Admin user management.
        Returns list sorted by created_at descending.
        """
        return list(
            mongo.db[UserModel.COLLECTION].find().sort('created_at', -1)
        )

    # ── Count helpers for admin dashboard ─────────────────────────────────────

    @staticmethod
    def count_all():
        """Total user count for admin dashboard."""
        return mongo.db[UserModel.COLLECTION].count_documents({})

    @staticmethod
    def count_by_role(role):
        """Count users by role (student/teacher/admin)."""
        return mongo.db[UserModel.COLLECTION].count_documents({'role': role})

    # ── Update ────────────────────────────────────────────────────────────────

    @staticmethod
    def update_password(user_id, new_hash):
        """
        changePassword() : Boolean – Update password hash.
        REQ-4.1.4, D-SEC-02: bcrypt hash stored, never plaintext.
        """
        return mongo.db[UserModel.COLLECTION].update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'password_hash': new_hash}}
        )

    @staticmethod
    def set_active_status(user_id, is_active):
        """
        disableUser() / enableUser() – Toggle account active state.
        REQ-4.1.5, D-SQ-05: User.update(is_active=False)
        """
        return mongo.db[UserModel.COLLECTION].update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'is_active': is_active}}
        )

    @staticmethod
    def update_role(user_id, new_role):
        """
        assignRole() – Change user role. REQ-4.1.5.
        Allowed values: 'student', 'teacher', 'admin'
        """
        return mongo.db[UserModel.COLLECTION].update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'role': new_role}}
        )
