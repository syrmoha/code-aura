import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask import Flask
from src.models.database import db, User, Course, CourseSection, CourseLesson
from src.models.database import Quiz, QuizQuestion, Article, Game, AITool, Category
from src.models.database import CourseRating, UserQuizAttempt, Forum, ForumPost
from src.models.database import UserGameScore, UserCourseProgress, Comment

def create_app():
    """Create Flask app for checking data"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 
        f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'code_aura_dev.db')}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    return app

def check_data():
    """Check existing data in the database"""
    print("Checking existing data...")
    
    # Check categories
    categories = Category.query.all()
    print(f"Categories: {len(categories)}")
    for category in categories:
        print(f"  - {category.id}: {category.name}")
    
    # Check users
    users = User.query.all()
    print(f"\nUsers: {len(users)}")
    for user in users:
        print(f"  - {user.id}: {user.username} ({user.email}) - Role: {user.role}")
    
    # Check courses
    courses = Course.query.all()
    print(f"\nCourses: {len(courses)}")
    for course in courses:
        print(f"  - {course.id}: {course.title} - Language: {course.language}")
    
    # Check quizzes
    quizzes = Quiz.query.all()
    print(f"\nQuizzes: {len(quizzes)}")
    for quiz in quizzes:
        print(f"  - {quiz.id}: {quiz.title}")
    
    # Check articles
    articles = Article.query.all()
    print(f"\nArticles: {len(articles)}")
    for article in articles:
        print(f"  - {article.id}: {article.title}")
    
    # Check games
    games = Game.query.all()
    print(f"\nGames: {len(games)}")
    for game in games:
        print(f"  - {game.id}: {game.title}")
    
    # Check AI tools
    ai_tools = AITool.query.all()
    print(f"\nAI Tools: {len(ai_tools)}")
    for tool in ai_tools:
        print(f"  - {tool.id}: {tool.name} - Type: {tool.tool_type}")
    
    # Check forums
    forums = Forum.query.all()
    print(f"\nForums: {len(forums)}")
    for forum in forums:
        print(f"  - {forum.id}: {forum.name}")

def main():
    """Main function to check data"""
    app = create_app()
    
    with app.app_context():
        check_data()

if __name__ == "__main__":
    main()

