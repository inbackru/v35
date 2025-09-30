#!/usr/bin/env python3
"""
Update script to add developer appointments system
"""

from app import db, app
from models import User, Manager

def update_user_assignments():
    """Auto-assign users to managers"""
    with app.app_context():
        # Get all users without managers
        unassigned_users = User.query.filter_by(assigned_manager_id=None).all()
        
        # Get first active manager
        manager = Manager.query.filter_by(is_active=True).first()
        
        if manager:
            for user in unassigned_users:
                user.assigned_manager_id = manager.id
                user.client_status = 'Новый'
            
            db.session.commit()
            print(f"Assigned {len(unassigned_users)} users to manager {manager.full_name}")
        else:
            print("No active managers found")

if __name__ == "__main__":
    update_user_assignments()