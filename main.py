import os
import sys
from datetime import timedelta
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.models.database import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp, init_auth_oauth
from src.routes.course import course_bp
from src.routes.quiz import quiz_bp
from src.routes.article import article_bp
from src.routes.game import game_bp
from src.routes.ai_tool import ai_tool_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'code-aura-secret-key-2024')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string-code-aura')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Database configuration - SQLite for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 
    f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'code_aura_dev.db')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app, origins="*")  # Allow all origins for development
jwt = JWTManager(app)
db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(course_bp, url_prefix='/api')
app.register_blueprint(quiz_bp, url_prefix='/api')
app.register_blueprint(article_bp, url_prefix='/api')
app.register_blueprint(game_bp, url_prefix='/api')
app.register_blueprint(ai_tool_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')

# Initialize OAuth for auth blueprint
init_auth_oauth(app)

# Create database tables
with app.app_context():
    db.create_all()

# Admin dashboard route
@app.route('/admin')
def admin_dashboard():
    return send_from_directory(app.static_folder, 'admin/index.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

