"""
dummy data 
FnB - Database Connection Module
Author: Manav
SRS Reference: Section 5.3 - Database Schema, Section 2.1 - MongoDB (Data Layer)
D-DB-01: users collection
D-DB-02: projects collection
D-DB-03: feedback collection
D-SEC-09: MongoDB dedicated app user with minimum privileges
D-ARCH-01: Data Layer (MongoDB Database)
"""

from flask_pymongo import PyMongo

# Single PyMongo instance shared across all models
mongo = PyMongo()