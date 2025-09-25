import os
from authlib.integrations.flask_client import OAuth

def init_oauth(app):
    """Initialize OAuth providers"""
    oauth = OAuth(app)
    
    # Google OAuth
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
    # Facebook OAuth
    facebook = oauth.register(
        name='facebook',
        client_id=os.getenv('FACEBOOK_CLIENT_ID'),
        client_secret=os.getenv('FACEBOOK_CLIENT_SECRET'),
        access_token_url='https://graph.facebook.com/oauth/access_token',
        authorize_url='https://www.facebook.com/dialog/oauth',
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email public_profile'},
    )
    
    # GitHub OAuth
    github = oauth.register(
        name='github',
        client_id=os.getenv('GITHUB_CLIENT_ID'),
        client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )
    
    return oauth, google, facebook, github

# OAuth provider configurations
OAUTH_PROVIDERS = {
    'google': {
        'name': 'Google',
        'icon': 'fab fa-google',
        'color': '#db4437'
    },
    'facebook': {
        'name': 'Facebook', 
        'icon': 'fab fa-facebook-f',
        'color': '#3b5998'
    },
    'github': {
        'name': 'GitHub',
        'icon': 'fab fa-github',
        'color': '#333'
    }
}

