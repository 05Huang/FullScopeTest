#!/usr/bin/env python
"""Initialize database with all tables."""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db

def init_database():
    """Create all database tables."""
    app = create_app('development')
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        # Create admin user
        from app.models.user import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                username='admin',
                email='admin@fullscopetest.com',
                is_admin=True,
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin / admin123")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_database()
