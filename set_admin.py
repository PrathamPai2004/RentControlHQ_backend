"""
Run this script from the backend directory to promote your account to admin:
  cd backend
  python set_admin.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models.user import User

app = create_app()

with app.app_context():
    email = 'prathameshpai.sdmcet26@gmail.com'
    user = User.query.filter_by(email=email).first()
    if user:
        user.role = 'admin'
        db.session.commit()
        print(f"✅ Success! '{email}' is now role=admin")
    else:
        print(f"❌ User '{email}' not found in the database")
