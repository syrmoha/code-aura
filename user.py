from src.models.database import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime

def create_user(username, email, password, bio=None, profile_picture_url=None):
    """Create a new user"""
    password_hash = generate_password_hash(password)
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        bio=bio,
        profile_picture_url=profile_picture_url
    )
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    """Authenticate user and return access token"""
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        user.last_login = datetime.utcnow()
        db.session.commit()
        access_token = create_access_token(identity=user.id)
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bio': user.bio,
                'profile_picture_url': user.profile_picture_url,
                'role': user.role
            }
        }
    return None

def get_user_by_id(user_id):
    """Get user by ID"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Get user by email"""
    return User.query.filter_by(email=email).first()

def update_user_profile(user_id, **kwargs):
    """Update user profile"""
    user = User.query.get(user_id)
    if user:
        for key, value in kwargs.items():
            if hasattr(user, key) and key != 'password_hash':
                setattr(user, key, value)
        db.session.commit()
        return user
    return None

def change_user_password(user_id, old_password, new_password):
    """Change user password"""
    user = User.query.get(user_id)
    if user and check_password_hash(user.password_hash, old_password):
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return True
    return False

