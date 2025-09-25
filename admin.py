from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, User, Course, CourseSection, CourseLesson, Quiz, QuizQuestion, Article, Game, AITool
from src.models.database import Category, Comment, CommunityPost, Forum, ForumPost, CourseRating, UserQuizAttempt, UserGameScore
from src.models.user import get_user_by_id
from werkzeug.security import generate_password_hash
import datetime
from sqlalchemy import func, desc

admin_bp = Blueprint('admin', __name__)

# Admin middleware to check if user is admin
def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = get_user_by_id(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return fn(*args, **kwargs)
    
    wrapper.__name__ = fn.__name__
    return wrapper

@admin_bp.route('/admin/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    """Get admin dashboard statistics"""
    try:
        # Get counts
        user_count = User.query.count()
        course_count = Course.query.count()
        quiz_count = Quiz.query.count()
        article_count = Article.query.count()
        game_count = Game.query.count()
        ai_tool_count = AITool.query.count()
        
        # Get recent users
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_users_list = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat() if user.created_at else None
        } for user in recent_users]
        
        # Get recent courses
        recent_courses = Course.query.order_by(Course.created_at.desc()).limit(5).all()
        recent_courses_list = [{
            'id': course.id,
            'title': course.title,
            'language': course.language,
            'level': course.level,
            'created_at': course.created_at.isoformat() if course.created_at else None
        } for course in recent_courses]
        
        return jsonify({
            'statistics': {
                'user_count': user_count,
                'course_count': course_count,
                'quiz_count': quiz_count,
                'article_count': article_count,
                'game_count': game_count,
                'ai_tool_count': ai_tool_count
            },
            'recent_users': recent_users_list,
            'recent_courses': recent_courses_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def admin_get_users():
    """Get all users (admin view)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        users = User.query.paginate(page=page, per_page=per_page, error_out=False)
        
        users_list = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'profile_picture_url': user.profile_picture_url,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        } for user in users.items]
        
        return jsonify({
            'users': users_list,
            'pagination': {
                'page': users.page,
                'pages': users.pages,
                'per_page': users.per_page,
                'total': users.total,
                'has_next': users.has_next,
                'has_prev': users.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@admin_required
def admin_update_user(user_id):
    """Update user (admin view)"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        
        # Update fields
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'role' in data and data['role'] in ['user', 'admin']:
            user.role = data['role']
        if 'profile_picture_url' in data:
            user.profile_picture_url = data['profile_picture_url']
        if 'bio' in data:
            user.bio = data['bio']
        if 'password' in data and data['password']:
            user.password_hash = generate_password_hash(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'profile_picture_url': user.profile_picture_url,
                'bio': user.bio
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def admin_delete_user(user_id):
    """Delete user (admin view)"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Don't allow deleting self
        current_user_id = get_jwt_identity()
        if user_id == current_user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/courses', methods=['GET'])
@admin_required
def admin_get_courses():
    """Get all courses (admin view)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        courses = Course.query.paginate(page=page, per_page=per_page, error_out=False)
        
        courses_list = [{
            'id': course.id,
            'title': course.title,
            'language': course.language,
            'level': course.level,
            'programming_language': course.programming_language,
            'youtube_video_id': course.youtube_video_id,
            'created_at': course.created_at.isoformat() if course.created_at else None,
            'sections_count': len(course.sections)
        } for course in courses.items]
        
        return jsonify({
            'courses': courses_list,
            'pagination': {
                'page': courses.page,
                'pages': courses.pages,
                'per_page': courses.per_page,
                'total': courses.total,
                'has_next': courses.has_next,
                'has_prev': courses.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/courses', methods=['POST'])
@admin_required
def admin_create_course():
    """Create new course (admin view)"""
    try:
        data = request.json
        
        # Validate required fields
        if not all(k in data for k in ('title', 'youtube_video_id', 'language', 'level')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create course
        course = Course(
            title=data['title'],
            description=data.get('description'),
            youtube_video_id=data['youtube_video_id'],
            youtube_playlist_id=data.get('youtube_playlist_id'),
            language=data['language'],
            level=data['level'],
            programming_language=data.get('programming_language'),
            duration_minutes=data.get('duration_minutes'),
            instructor_name=data.get('instructor_name')
        )
        
        # Add categories if provided
        if 'category_ids' in data and isinstance(data['category_ids'], list):
            from src.models.database import Category
            categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
            course.categories = categories
        
        db.session.add(course)
        db.session.commit()
        
        return jsonify({
            'message': 'Course created successfully',
            'course': {
                'id': course.id,
                'title': course.title
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/courses/<int:course_id>', methods=['PUT'])
@admin_required
def admin_update_course(course_id):
    """Update course (admin view)"""
    try:
        course = Course.query.get_or_404(course_id)
        data = request.json
        
        # Update fields
        if 'title' in data:
            course.title = data['title']
        if 'description' in data:
            course.description = data['description']
        if 'youtube_video_id' in data:
            course.youtube_video_id = data['youtube_video_id']
        if 'youtube_playlist_id' in data:
            course.youtube_playlist_id = data['youtube_playlist_id']
        if 'language' in data:
            course.language = data['language']
        if 'level' in data:
            course.level = data['level']
        if 'programming_language' in data:
            course.programming_language = data['programming_language']
        if 'duration_minutes' in data:
            course.duration_minutes = data['duration_minutes']
        if 'instructor_name' in data:
            course.instructor_name = data['instructor_name']
        
        # Update categories if provided
        if 'category_ids' in data and isinstance(data['category_ids'], list):
            from src.models.database import Category
            categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
            course.categories = categories
        
        course.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Course updated successfully',
            'course': {
                'id': course.id,
                'title': course.title
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/courses/<int:course_id>', methods=['DELETE'])
@admin_required
def admin_delete_course(course_id):
    """Delete course (admin view)"""
    try:
        course = Course.query.get_or_404(course_id)
        
        db.session.delete(course)
        db.session.commit()
        
        return jsonify({
            'message': 'Course deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/create-admin', methods=['POST'])
@admin_required
def create_admin_user():
    """Create a new admin user (admin only)"""
    try:
        data = request.json
        
        # Validate required fields
        if not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter((User.email == data['email']) | 
                                         (User.username == data['username'])).first()
        if existing_user:
            return jsonify({'error': 'User with this email or username already exists'}), 400
        
        # Create admin user
        admin_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            bio=data.get('bio', 'Administrator'),
            profile_picture_url=data.get('profile_picture_url'),
            role='admin'
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Admin user created successfully',
            'user': {
                'id': admin_user.id,
                'username': admin_user.username,
                'email': admin_user.email,
                'role': admin_user.role
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Home Page Management
@admin_bp.route('/admin/homepage', methods=['GET'])
@admin_required
def admin_get_homepage_settings():
    """Get homepage settings"""
    try:
        # Get featured courses
        featured_courses = db.session.query(
            Course,
            func.avg(CourseRating.rating).label('avg_rating'),
            func.count(CourseRating.id).label('rating_count')
        ).outerjoin(CourseRating).group_by(Course.id).order_by(
            func.avg(CourseRating.rating).desc()
        ).limit(6).all()
        
        featured_courses_list = []
        for course, avg_rating, rating_count in featured_courses:
            featured_courses_list.append({
                'id': course.id,
                'title': course.title,
                'language': course.language,
                'level': course.level,
                'youtube_video_id': course.youtube_video_id,
                'average_rating': round(float(avg_rating), 1) if avg_rating else 0,
                'rating_count': rating_count or 0
            })
        
        # Get latest articles
        latest_articles = Article.query.filter_by(is_published=True).order_by(
            Article.created_at.desc()
        ).limit(5).all()
        
        latest_articles_list = []
        for article in latest_articles:
            latest_articles_list.append({
                'id': article.id,
                'title': article.title,
                'author': article.author.username if article.author else None,
                'created_at': article.created_at.isoformat() if article.created_at else None
            })
        
        # Get top categories
        top_categories = db.session.query(
            Category,
            func.count(CourseCategory.course_id).label('course_count')
        ).join(CourseCategory).group_by(Category.id).order_by(
            func.count(CourseCategory.course_id).desc()
        ).limit(10).all()
        
        top_categories_list = []
        for category, course_count in top_categories:
            top_categories_list.append({
                'id': category.id,
                'name': category.name,
                'course_count': course_count
            })
        
        return jsonify({
            'featured_courses': featured_courses_list,
            'latest_articles': latest_articles_list,
            'top_categories': top_categories_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/homepage/banner', methods=['PUT'])
@admin_required
def admin_update_homepage_banner():
    """Update homepage banner"""
    try:
        data = request.json
        
        # In a real implementation, this would update a settings table
        # For now, we'll just return success
        
        return jsonify({
            'message': 'Homepage banner updated successfully',
            'banner': data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Category Management
@admin_bp.route('/admin/categories', methods=['GET'])
@admin_required
def admin_get_categories():
    """Get all categories"""
    try:
        categories = Category.query.all()
        
        categories_list = []
        for category in categories:
            course_count = db.session.query(func.count(CourseCategory.course_id)).filter(
                CourseCategory.category_id == category.id
            ).scalar()
            
            article_count = db.session.query(func.count(ArticleCategory.article_id)).filter(
                ArticleCategory.category_id == category.id
            ).scalar()
            
            categories_list.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'course_count': course_count or 0,
                'article_count': article_count or 0
            })
        
        return jsonify({
            'categories': categories_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/categories', methods=['POST'])
@admin_required
def admin_create_category():
    """Create new category"""
    try:
        data = request.json
        
        if 'name' not in data:
            return jsonify({'error': 'Category name is required'}), 400
        
        # Check if category already exists
        existing_category = Category.query.filter_by(name=data['name']).first()
        if existing_category:
            return jsonify({'error': 'Category with this name already exists'}), 400
        
        # Create category
        category = Category(
            name=data['name'],
            description=data.get('description')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/categories/<int:category_id>', methods=['PUT'])
@admin_required
def admin_update_category(category_id):
    """Update category"""
    try:
        category = Category.query.get_or_404(category_id)
        data = request.json
        
        if 'name' in data:
            # Check if name is already taken by another category
            existing_category = Category.query.filter_by(name=data['name']).first()
            if existing_category and existing_category.id != category_id:
                return jsonify({'error': 'Category with this name already exists'}), 400
            
            category.name = data['name']
        
        if 'description' in data:
            category.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Category updated successfully',
            'category': {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def admin_delete_category(category_id):
    """Delete category"""
    try:
        category = Category.query.get_or_404(category_id)
        
        # Check if category is used by courses or articles
        course_count = db.session.query(func.count(CourseCategory.course_id)).filter(
            CourseCategory.category_id == category_id
        ).scalar()
        
        article_count = db.session.query(func.count(ArticleCategory.article_id)).filter(
            ArticleCategory.category_id == category_id
        ).scalar()
        
        if course_count > 0 or article_count > 0:
            return jsonify({
                'error': f'Cannot delete category. It is used by {course_count} courses and {article_count} articles'
            }), 400
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Quiz Management
@admin_bp.route('/admin/quizzes', methods=['GET'])
@admin_required
def admin_get_quizzes():
    """Get all quizzes (admin view)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        quizzes = Quiz.query.paginate(page=page, per_page=per_page, error_out=False)
        
        quizzes_list = []
        for quiz in quizzes.items:
            # Get question count
            question_count = QuizQuestion.query.filter_by(quiz_id=quiz.id).count()
            
            # Get attempt count
            attempt_count = UserQuizAttempt.query.filter_by(quiz_id=quiz.id).count()
            
            quizzes_list.append({
                'id': quiz.id,
                'title': quiz.title,
                'programming_language': quiz.programming_language,
                'level': quiz.level,
                'question_count': question_count,
                'time_limit_minutes': quiz.time_limit_minutes,
                'created_at': quiz.created_at.isoformat() if quiz.created_at else None,
                'attempt_count': attempt_count
            })
        
        return jsonify({
            'quizzes': quizzes_list,
            'pagination': {
                'page': quizzes.page,
                'pages': quizzes.pages,
                'per_page': quizzes.per_page,
                'total': quizzes.total,
                'has_next': quizzes.has_next,
                'has_prev': quizzes.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/quizzes', methods=['POST'])
@admin_required
def admin_create_quiz():
    """Create new quiz (admin view)"""
    try:
        data = request.json
        
        # Validate required fields
        if not all(k in data for k in ('title', 'programming_language', 'level')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create quiz
        quiz = Quiz(
            title=data['title'],
            description=data.get('description'),
            programming_language=data['programming_language'],
            level=data['level'],
            question_count=data.get('question_count', 10),
            time_limit_minutes=data.get('time_limit_minutes', 30)
        )
        
        db.session.add(quiz)
        db.session.commit()
        
        return jsonify({
            'message': 'Quiz created successfully',
            'quiz': {
                'id': quiz.id,
                'title': quiz.title
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/quizzes/<int:quiz_id>', methods=['PUT'])
@admin_required
def admin_update_quiz(quiz_id):
    """Update quiz (admin view)"""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        data = request.json
        
        # Update fields
        if 'title' in data:
            quiz.title = data['title']
        if 'description' in data:
            quiz.description = data['description']
        if 'programming_language' in data:
            quiz.programming_language = data['programming_language']
        if 'level' in data:
            quiz.level = data['level']
        if 'question_count' in data:
            quiz.question_count = data['question_count']
        if 'time_limit_minutes' in data:
            quiz.time_limit_minutes = data['time_limit_minutes']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Quiz updated successfully',
            'quiz': {
                'id': quiz.id,
                'title': quiz.title
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/quizzes/<int:quiz_id>', methods=['DELETE'])
@admin_required
def admin_delete_quiz(quiz_id):
    """Delete quiz (admin view)"""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        
        # Delete all questions first
        QuizQuestion.query.filter_by(quiz_id=quiz_id).delete()
        
        # Delete all attempts
        UserQuizAttempt.query.filter_by(quiz_id=quiz_id).delete()
        
        # Delete quiz
        db.session.delete(quiz)
        db.session.commit()
        
        return jsonify({
            'message': 'Quiz deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/quizzes/<int:quiz_id>/questions', methods=['GET'])
@admin_required
def admin_get_quiz_questions(quiz_id):
    """Get quiz questions (admin view)"""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        
        questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
        
        questions_list = []
        for question in questions:
            questions_list.append({
                'id': question.id,
                'question_text': question.question_text,
                'question_type': question.question_type,
                'code_snippet': question.code_snippet,
                'correct_answer': question.correct_answer,
                'options': question.options,
                'explanation': question.explanation,
                'difficulty_points': question.difficulty_points
            })
        
        return jsonify({
            'quiz': {
                'id': quiz.id,
                'title': quiz.title
            },
            'questions': questions_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/quizzes/<int:quiz_id>/questions', methods=['POST'])
@admin_required
def admin_create_quiz_question(quiz_id):
    """Create new quiz question (admin view)"""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        data = request.json
        
        # Validate required fields
        if not all(k in data for k in ('question_text', 'question_type')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create question
        question = QuizQuestion(
            quiz_id=quiz_id,
            question_text=data['question_text'],
            question_type=data['question_type'],
            code_snippet=data.get('code_snippet'),
            correct_answer=data.get('correct_answer'),
            options=data.get('options'),
            explanation=data.get('explanation'),
            difficulty_points=data.get('difficulty_points', 1)
        )
        
        db.session.add(question)
        db.session.commit()
        
        return jsonify({
            'message': 'Question created successfully',
            'question': {
                'id': question.id,
                'question_text': question.question_text
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/quizzes/questions/<int:question_id>', methods=['PUT'])
@admin_required
def admin_update_quiz_question(question_id):
    """Update quiz question (admin view)"""
    try:
        question = QuizQuestion.query.get_or_404(question_id)
        data = request.json
        
        # Update fields
        if 'question_text' in data:
            question.question_text = data['question_text']
        if 'question_type' in data:
            question.question_type = data['question_type']
        if 'code_snippet' in data:
            question.code_snippet = data['code_snippet']
        if 'correct_answer' in data:
            question.correct_answer = data['correct_answer']
        if 'options' in data:
            question.options = data['options']
        if 'explanation' in data:
            question.explanation = data['explanation']
        if 'difficulty_points' in data:
            question.difficulty_points = data['difficulty_points']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Question updated successfully',
            'question': {
                'id': question.id,
                'question_text': question.question_text
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/quizzes/questions/<int:question_id>', methods=['DELETE'])
@admin_required
def admin_delete_quiz_question(question_id):
    """Delete quiz question (admin view)"""
    try:
        question = QuizQuestion.query.get_or_404(question_id)
        
        db.session.delete(question)
        db.session.commit()
        
        return jsonify({
            'message': 'Question deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Game Management
@admin_bp.route('/admin/games', methods=['GET'])
@admin_required
def admin_get_games():
    """Get all games (admin view)"""
    try:
        games = Game.query.all()
        
        games_list = []
        for game in games:
            # Get play count
            play_count = UserGameScore.query.filter_by(game_id=game.id).count()
            
            games_list.append({
                'id': game.id,
                'title': game.title,
                'description': game.description,
                'game_url': game.game_url,
                'created_at': game.created_at.isoformat() if game.created_at else None,
                'play_count': play_count
            })
        
        return jsonify({
            'games': games_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/games', methods=['POST'])
@admin_required
def admin_create_game():
    """Create new game (admin view)"""
    try:
        data = request.json
        
        # Validate required fields
        if not all(k in data for k in ('title', 'game_url')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create game
        game = Game(
            title=data['title'],
            description=data.get('description'),
            game_url=data['game_url']
        )
        
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'message': 'Game created successfully',
            'game': {
                'id': game.id,
                'title': game.title
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/games/<int:game_id>', methods=['PUT'])
@admin_required
def admin_update_game(game_id):
    """Update game (admin view)"""
    try:
        game = Game.query.get_or_404(game_id)
        data = request.json
        
        # Update fields
        if 'title' in data:
            game.title = data['title']
        if 'description' in data:
            game.description = data['description']
        if 'game_url' in data:
            game.game_url = data['game_url']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Game updated successfully',
            'game': {
                'id': game.id,
                'title': game.title
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/games/<int:game_id>', methods=['DELETE'])
@admin_required
def admin_delete_game(game_id):
    """Delete game (admin view)"""
    try:
        game = Game.query.get_or_404(game_id)
        
        # Delete all scores first
        UserGameScore.query.filter_by(game_id=game_id).delete()
        
        # Delete game
        db.session.delete(game)
        db.session.commit()
        
        return jsonify({
            'message': 'Game deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# AI Tools Management
@admin_bp.route('/admin/ai-tools', methods=['GET'])
@admin_required
def admin_get_ai_tools():
    """Get all AI tools (admin view)"""
    try:
        ai_tools = AITool.query.all()
        
        ai_tools_list = []
        for tool in ai_tools:
            ai_tools_list.append({
                'id': tool.id,
                'name': tool.name,
                'description': tool.description,
                'api_endpoint': tool.api_endpoint,
                'tool_type': tool.tool_type,
                'created_at': tool.created_at.isoformat() if tool.created_at else None
            })
        
        return jsonify({
            'ai_tools': ai_tools_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/ai-tools', methods=['POST'])
@admin_required
def admin_create_ai_tool():
    """Create new AI tool (admin view)"""
    try:
        data = request.json
        
        # Validate required fields
        if not all(k in data for k in ('name', 'tool_type')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create AI tool
        ai_tool = AITool(
            name=data['name'],
            description=data.get('description'),
            api_endpoint=data.get('api_endpoint'),
            tool_type=data['tool_type']
        )
        
        db.session.add(ai_tool)
        db.session.commit()
        
        return jsonify({
            'message': 'AI tool created successfully',
            'ai_tool': {
                'id': ai_tool.id,
                'name': ai_tool.name
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/ai-tools/<int:ai_tool_id>', methods=['PUT'])
@admin_required
def admin_update_ai_tool(ai_tool_id):
    """Update AI tool (admin view)"""
    try:
        ai_tool = AITool.query.get_or_404(ai_tool_id)
        data = request.json
        
        # Update fields
        if 'name' in data:
            ai_tool.name = data['name']
        if 'description' in data:
            ai_tool.description = data['description']
        if 'api_endpoint' in data:
            ai_tool.api_endpoint = data['api_endpoint']
        if 'tool_type' in data:
            ai_tool.tool_type = data['tool_type']
        
        db.session.commit()
        
        return jsonify({
            'message': 'AI tool updated successfully',
            'ai_tool': {
                'id': ai_tool.id,
                'name': ai_tool.name
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/ai-tools/<int:ai_tool_id>', methods=['DELETE'])
@admin_required
def admin_delete_ai_tool(ai_tool_id):
    """Delete AI tool (admin view)"""
    try:
        ai_tool = AITool.query.get_or_404(ai_tool_id)
        
        db.session.delete(ai_tool)
        db.session.commit()
        
        return jsonify({
            'message': 'AI tool deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Article Management
@admin_bp.route('/admin/articles', methods=['GET'])
@admin_required
def admin_get_articles():
    """Get all articles (admin view)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        articles = Article.query.paginate(page=page, per_page=per_page, error_out=False)
        
        articles_list = []
        for article in articles.items:
            # Get comment count
            comment_count = Comment.query.filter_by(
                commentable_type='article',
                commentable_id=article.id
            ).count()
            
            articles_list.append({
                'id': article.id,
                'title': article.title,
                'author_id': article.author_id,
                'author_name': article.author.username if article.author else None,
                'created_at': article.created_at.isoformat() if article.created_at else None,
                'updated_at': article.updated_at.isoformat() if article.updated_at else None,
                'is_published': article.is_published,
                'comment_count': comment_count,
                'categories': [{'id': cat.id, 'name': cat.name} for cat in article.categories]
            })
        
        return jsonify({
            'articles': articles_list,
            'pagination': {
                'page': articles.page,
                'pages': articles.pages,
                'per_page': articles.per_page,
                'total': articles.total,
                'has_next': articles.has_next,
                'has_prev': articles.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/articles', methods=['POST'])
@admin_required
def admin_create_article():
    """Create new article (admin view)"""
    try:
        data = request.json
        user_id = get_jwt_identity()
        
        # Validate required fields
        if not all(k in data for k in ('title', 'content')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create article
        article = Article(
            title=data['title'],
            content=data['content'],
            author_id=data.get('author_id', user_id),
            is_published=data.get('is_published', True)
        )
        
        # Add categories if provided
        if 'category_ids' in data and isinstance(data['category_ids'], list):
            categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
            article.categories = categories
        
        db.session.add(article)
        db.session.commit()
        
        return jsonify({
            'message': 'Article created successfully',
            'article': {
                'id': article.id,
                'title': article.title
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/articles/<int:article_id>', methods=['PUT'])
@admin_required
def admin_update_article(article_id):
    """Update article (admin view)"""
    try:
        article = Article.query.get_or_404(article_id)
        data = request.json
        
        # Update fields
        if 'title' in data:
            article.title = data['title']
        if 'content' in data:
            article.content = data['content']
        if 'author_id' in data:
            article.author_id = data['author_id']
        if 'is_published' in data:
            article.is_published = data['is_published']
        
        # Update categories if provided
        if 'category_ids' in data and isinstance(data['category_ids'], list):
            categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
            article.categories = categories
        
        article.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Article updated successfully',
            'article': {
                'id': article.id,
                'title': article.title
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/articles/<int:article_id>', methods=['DELETE'])
@admin_required
def admin_delete_article(article_id):
    """Delete article (admin view)"""
    try:
        article = Article.query.get_or_404(article_id)
        
        # Delete all comments first
        Comment.query.filter_by(
            commentable_type='article',
            commentable_id=article_id
        ).delete()
        
        # Delete article
        db.session.delete(article)
        db.session.commit()
        
        return jsonify({
            'message': 'Article deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Forum Management
@admin_bp.route('/admin/forums', methods=['GET'])
@admin_required
def admin_get_forums():
    """Get all forums (admin view)"""
    try:
        forums = Forum.query.all()
        
        forums_list = []
        for forum in forums:
            # Get post count
            post_count = ForumPost.query.filter_by(forum_id=forum.id, parent_post_id=None).count()
            
            forums_list.append({
                'id': forum.id,
                'name': forum.name,
                'description': forum.description,
                'category_id': forum.category_id,
                'category_name': forum.category.name if forum.category else None,
                'created_at': forum.created_at.isoformat() if forum.created_at else None,
                'post_count': post_count
            })
        
        return jsonify({
            'forums': forums_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/forums', methods=['POST'])
@admin_required
def admin_create_forum():
    """Create new forum (admin view)"""
    try:
        data = request.json
        
        # Validate required fields
        if not all(k in data for k in ('name', 'category_id')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if category exists
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Create forum
        forum = Forum(
            name=data['name'],
            description=data.get('description'),
            category_id=data['category_id']
        )
        
        db.session.add(forum)
        db.session.commit()
        
        return jsonify({
            'message': 'Forum created successfully',
            'forum': {
                'id': forum.id,
                'name': forum.name
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/forums/<int:forum_id>', methods=['PUT'])
@admin_required
def admin_update_forum(forum_id):
    """Update forum (admin view)"""
    try:
        forum = Forum.query.get_or_404(forum_id)
        data = request.json
        
        # Update fields
        if 'name' in data:
            forum.name = data['name']
        if 'description' in data:
            forum.description = data['description']
        if 'category_id' in data:
            # Check if category exists
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({'error': 'Category not found'}), 404
            
            forum.category_id = data['category_id']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Forum updated successfully',
            'forum': {
                'id': forum.id,
                'name': forum.name
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/forums/<int:forum_id>', methods=['DELETE'])
@admin_required
def admin_delete_forum(forum_id):
    """Delete forum (admin view)"""
    try:
        forum = Forum.query.get_or_404(forum_id)
        
        # Check if forum has posts
        post_count = ForumPost.query.filter_by(forum_id=forum_id).count()
        if post_count > 0:
            return jsonify({
                'error': f'Cannot delete forum. It contains {post_count} posts'
            }), 400
        
        # Delete forum
        db.session.delete(forum)
        db.session.commit()
        
        return jsonify({
            'message': 'Forum deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/forums/<int:forum_id>/posts', methods=['GET'])
@admin_required
def admin_get_forum_posts(forum_id):
    """Get forum posts (admin view)"""
    try:
        forum = Forum.query.get_or_404(forum_id)
        
        # Get top-level posts (no parent)
        posts = ForumPost.query.filter_by(forum_id=forum_id, parent_post_id=None).order_by(
            ForumPost.created_at.desc()
        ).all()
        
        posts_list = []
        for post in posts:
            # Get reply count
            reply_count = ForumPost.query.filter_by(parent_post_id=post.id).count()
            
            posts_list.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'user_id': post.user_id,
                'username': post.user.username if post.user else None,
                'created_at': post.created_at.isoformat() if post.created_at else None,
                'reply_count': reply_count
            })
        
        return jsonify({
            'forum': {
                'id': forum.id,
                'name': forum.name
            },
            'posts': posts_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/forum-posts/<int:post_id>', methods=['DELETE'])
@admin_required
def admin_delete_forum_post(post_id):
    """Delete forum post (admin view)"""
    try:
        post = ForumPost.query.get_or_404(post_id)
        
        # Delete all replies first
        ForumPost.query.filter_by(parent_post_id=post_id).delete()
        
        # Delete post
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({
            'message': 'Forum post deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Statistics and Analytics
@admin_bp.route('/admin/statistics', methods=['GET'])
@admin_required
def admin_get_statistics():
    """Get site statistics (admin view)"""
    try:
        # User statistics
        total_users = User.query.count()
        admin_users = User.query.filter_by(role='admin').count()
        new_users_today = User.query.filter(
            User.created_at >= datetime.datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        ).count()
        
        # Content statistics
        total_courses = Course.query.count()
        total_quizzes = Quiz.query.count()
        total_articles = Article.query.count()
        total_games = Game.query.count()
        total_ai_tools = AITool.query.count()
        
        # Activity statistics
        course_progress_count = UserCourseProgress.query.count()
        quiz_attempts_count = UserQuizAttempt.query.count()
        game_scores_count = UserGameScore.query.count()
        
        # Language distribution
        arabic_courses = Course.query.filter_by(language='arabic').count()
        english_courses = Course.query.filter_by(language='english').count()
        other_courses = Course.query.filter_by(language='other').count()
        
        # Programming language distribution
        programming_languages = db.session.query(
            Course.programming_language,
            func.count(Course.id).label('count')
        ).filter(Course.programming_language.isnot(None)).group_by(
            Course.programming_language
        ).all()
        
        programming_languages_list = [
            {'language': lang, 'count': count} for lang, count in programming_languages
        ]
        
        # Monthly user registrations (last 6 months)
        now = datetime.datetime.utcnow()
        months = []
        for i in range(5, -1, -1):
            month_start = (now.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
            month_start = month_start.replace(month=(now.month - i) % 12 or 12)
            if now.month - i <= 0:
                month_start = month_start.replace(year=now.year - 1)
            
            next_month = month_start.replace(month=month_start.month % 12 + 1)
            if month_start.month == 12:
                next_month = next_month.replace(year=month_start.year + 1)
            
            count = User.query.filter(
                User.created_at >= month_start,
                User.created_at < next_month
            ).count()
            
            months.append({
                'month': month_start.strftime('%B %Y'),
                'count': count
            })
        
        return jsonify({
            'users': {
                'total': total_users,
                'admins': admin_users,
                'new_today': new_users_today,
                'monthly_registrations': months
            },
            'content': {
                'courses': total_courses,
                'quizzes': total_quizzes,
                'articles': total_articles,
                'games': total_games,
                'ai_tools': total_ai_tools
            },
            'activity': {
                'course_progress': course_progress_count,
                'quiz_attempts': quiz_attempts_count,
                'game_scores': game_scores_count
            },
            'languages': {
                'arabic': arabic_courses,
                'english': english_courses,
                'other': other_courses
            },
            'programming_languages': programming_languages_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

