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