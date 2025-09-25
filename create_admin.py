import os
import sys
import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask import Flask
from werkzeug.security import generate_password_hash
from src.models.database import db, User

def create_admin_user(username, email, password):
    """Create an admin user"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 
        f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'code_aura_dev.db')}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if user already exists
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        
        if existing_user:
            if existing_user.role == 'admin':
                print(f"Admin user {username} already exists. Updating password...")
                existing_user.password_hash = generate_password_hash(password)
                existing_user.last_login = datetime.datetime.utcnow()
                db.session.commit()
                print(f"Password updated for admin user: {username}")
                return
            else:
                print(f"User {username} exists but is not an admin. Upgrading to admin...")
                existing_user.role = 'admin'
                existing_user.password_hash = generate_password_hash(password)
                existing_user.last_login = datetime.datetime.utcnow()
                db.session.commit()
                print(f"User {username} upgraded to admin")
                return
        
        # Create new admin user
        admin_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            bio="Code Aura Administrator",
            role='admin',
            created_at=datetime.datetime.utcnow(),
            last_login=datetime.datetime.utcnow()
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"Admin user created successfully: {username}")

if __name__ == "__main__":
    # Default admin credentials
    admin_username = "admin"
    admin_email = "qaseemmohammad60@gmail.com"
    admin_password = "Mohammadabukashreef1#$"
    
    # Allow command line arguments to override defaults
    if len(sys.argv) > 1:
        admin_username = sys.argv[1]
    if len(sys.argv) > 2:
        admin_email = sys.argv[2]
    if len(sys.argv) > 3:
        admin_password = sys.argv[3]
    
    create_admin_user(admin_username, admin_email, admin_password)

