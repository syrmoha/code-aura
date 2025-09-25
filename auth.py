from flask import Blueprint, jsonify, request, redirect, url_for, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.database import db, User, UserOAuth
from src.models.user import create_user, authenticate_user, get_user_by_email
from src.config.oauth import init_oauth
from werkzeug.security import generate_password_hash
import secrets
import string

auth_bp = Blueprint('auth', __name__)

# Initialize OAuth (will be done in main.py)
oauth = None
google = None
facebook = None
github = None

def init_auth_oauth(app):
    """Initialize OAuth for auth blueprint"""
    global oauth, google, facebook, github
    oauth, google, facebook, github = init_oauth(app)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user with email/password"""
    try:
        data = request.json
        
        # Validate required fields
        if not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if get_user_by_email(data['email']):
            return jsonify({'error': 'Email already registered'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 400
        
        # Create user
        user = create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            bio=data.get('bio'),
            profile_picture_url=data.get('profile_picture_url')
        )
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bio': user.bio,
                'profile_picture_url': user.profile_picture_url,
                'role': user.role
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user with email/password"""
    try:
        data = request.json
        
        if not all(k in data for k in ('email', 'password')):
            return jsonify({'error': 'Missing email or password'}), 400
        
        result = authenticate_user(data['email'], data['password'])
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/<provider>/login', methods=['GET'])
def oauth_login(provider):
    """Initiate OAuth login"""
    try:
        if provider not in ['google', 'facebook', 'github']:
            return jsonify({'error': 'Unsupported provider'}), 400
        
        # Store the provider in session for callback
        session['oauth_provider'] = provider
        
        if provider == 'google':
            redirect_uri = url_for('auth.oauth_callback', provider='google', _external=True)
            return google.authorize_redirect(redirect_uri)
        elif provider == 'facebook':
            redirect_uri = url_for('auth.oauth_callback', provider='facebook', _external=True)
            return facebook.authorize_redirect(redirect_uri)
        elif provider == 'github':
            redirect_uri = url_for('auth.oauth_callback', provider='github', _external=True)
            return github.authorize_redirect(redirect_uri)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/<provider>/callback', methods=['GET'])
def oauth_callback(provider):
    """Handle OAuth callback"""
    try:
        if provider not in ['google', 'facebook', 'github']:
            return jsonify({'error': 'Unsupported provider'}), 400
        
        # Get OAuth client
        if provider == 'google':
            client = google
        elif provider == 'facebook':
            client = facebook
        elif provider == 'github':
            client = github
        
        # Get access token
        token = client.authorize_access_token()
        
        # Get user info from provider
        if provider == 'google':
            user_info = token.get('userinfo')
            if user_info:
                provider_user_id = user_info['sub']
                email = user_info['email']
                name = user_info['name']
                avatar = user_info.get('picture')
            else:
                return jsonify({'error': 'Failed to get user info from Google'}), 400
                
        elif provider == 'facebook':
            resp = client.get('me?fields=id,email,name,picture', token=token)
            user_info = resp.json()
            provider_user_id = user_info['id']
            email = user_info.get('email')
            name = user_info['name']
            avatar = user_info.get('picture', {}).get('data', {}).get('url')
            
        elif provider == 'github':
            resp = client.get('user', token=token)
            user_info = resp.json()
            provider_user_id = str(user_info['id'])
            email = user_info.get('email')
            name = user_info.get('name') or user_info.get('login')
            avatar = user_info.get('avatar_url')
            
            # GitHub might not return email in user endpoint
            if not email:
                emails_resp = client.get('user/emails', token=token)
                emails = emails_resp.json()
                primary_email = next((e['email'] for e in emails if e['primary']), None)
                email = primary_email
        
        if not email:
            return jsonify({'error': 'Email not provided by OAuth provider'}), 400
        
        # Check if OAuth account already exists
        oauth_account = UserOAuth.query.filter_by(
            provider=provider,
            provider_user_id=provider_user_id
        ).first()
        
        if oauth_account:
            # User exists, update OAuth info and login
            oauth_account.access_token = token.get('access_token')
            oauth_account.refresh_token = token.get('refresh_token')
            oauth_account.provider_email = email
            oauth_account.provider_name = name
            oauth_account.provider_avatar = avatar
            db.session.commit()
            
            user = oauth_account.user
        else:
            # Check if user exists with this email
            user = get_user_by_email(email)
            
            if not user:
                # Create new user
                # Generate random password for OAuth users
                random_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
                
                # Generate unique username from name/email
                base_username = name.lower().replace(' ', '_') if name else email.split('@')[0]
                username = base_username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base_username}_{counter}"
                    counter += 1
                
                user = User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(random_password),
                    profile_picture_url=avatar,
                    bio=f"Joined via {provider.title()}"
                )
                db.session.add(user)
                db.session.flush()  # Get user ID
            
            # Create OAuth account
            oauth_account = UserOAuth(
                user_id=user.id,
                provider=provider,
                provider_user_id=provider_user_id,
                provider_email=email,
                provider_name=name,
                provider_avatar=avatar,
                access_token=token.get('access_token'),
                refresh_token=token.get('refresh_token')
            )
            db.session.add(oauth_account)
            db.session.commit()
        
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        
        # Redirect to frontend with token (or return JSON for API)
        # For now, return JSON response
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bio': user.bio,
                'profile_picture_url': user.profile_picture_url,
                'role': user.role
            },
            'oauth_provider': provider
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get OAuth accounts
        oauth_accounts = []
        for oauth_account in user.oauth_accounts:
            oauth_accounts.append({
                'provider': oauth_account.provider,
                'provider_name': oauth_account.provider_name,
                'provider_avatar': oauth_account.provider_avatar,
                'created_at': oauth_account.created_at.isoformat() if oauth_account.created_at else None
            })
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'profile_picture_url': user.profile_picture_url,
            'role': user.role,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'oauth_accounts': oauth_accounts
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/providers', methods=['GET'])
def get_oauth_providers():
    """Get available OAuth providers"""
    from src.config.oauth import OAUTH_PROVIDERS
    
    return jsonify({
        'providers': OAUTH_PROVIDERS
    }), 200

