from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, Course, Category, CourseRating, UserCourseProgress
from sqlalchemy import func

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses', methods=['GET'])
def get_courses():
    """Get all courses with filters"""
    try:
        # Get query parameters
        language = request.args.get('language')
        level = request.args.get('level')
        programming_language = request.args.get('programming_language')
        category_id = request.args.get('category_id')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        query = Course.query
        
        if language:
            query = query.filter(Course.language == language)
        if level:
            query = query.filter(Course.level == level)
        if programming_language:
            query = query.filter(Course.programming_language == programming_language)
        if category_id:
            query = query.join(Course.categories).filter(Category.id == category_id)
        
        # Paginate
        courses = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Get average ratings for each course
        course_list = []
        for course in courses.items:
            avg_rating = db.session.query(func.avg(CourseRating.rating)).filter(
                CourseRating.course_id == course.id
            ).scalar()
            
            rating_count = db.session.query(func.count(CourseRating.id)).filter(
                CourseRating.course_id == course.id
            ).scalar()
            
            course_list.append({
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'youtube_video_id': course.youtube_video_id,
                'youtube_playlist_id': course.youtube_playlist_id,
                'language': course.language,
                'level': course.level,
                'programming_language': course.programming_language,
                'duration_minutes': course.duration_minutes,
                'instructor_name': course.instructor_name,
                'created_at': course.created_at.isoformat() if course.created_at else None,
                'categories': [{'id': cat.id, 'name': cat.name} for cat in course.categories],
                'average_rating': round(float(avg_rating), 1) if avg_rating else 0,
                'rating_count': rating_count or 0
            })
        
        return jsonify({
            'courses': course_list,
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

@course_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get single course details"""
    try:
        course = Course.query.get_or_404(course_id)
        
        # Get average rating
        avg_rating = db.session.query(func.avg(CourseRating.rating)).filter(
            CourseRating.course_id == course.id
        ).scalar()
        
        rating_count = db.session.query(func.count(CourseRating.id)).filter(
            CourseRating.course_id == course.id
        ).scalar()
        
        # Get recent ratings with user info
        recent_ratings = db.session.query(CourseRating).filter(
            CourseRating.course_id == course.id
        ).order_by(CourseRating.created_at.desc()).limit(5).all()
        
        ratings_list = []
        for rating in recent_ratings:
            ratings_list.append({
                'id': rating.id,
                'rating': rating.rating,
                'review_text': rating.review_text,
                'created_at': rating.created_at.isoformat() if rating.created_at else None,
                'user': {
                    'id': rating.user.id,
                    'username': rating.user.username,
                    'profile_picture_url': rating.user.profile_picture_url
                }
            })
        
        return jsonify({
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'youtube_video_id': course.youtube_video_id,
            'youtube_playlist_id': course.youtube_playlist_id,
            'language': course.language,
            'level': course.level,
            'programming_language': course.programming_language,
            'duration_minutes': course.duration_minutes,
            'instructor_name': course.instructor_name,
            'created_at': course.created_at.isoformat() if course.created_at else None,
            'categories': [{'id': cat.id, 'name': cat.name} for cat in course.categories],
            'sections': [{
                'id': section.id,
                'title': section.title,
                'order_index': section.order_index,
                'lessons': [{
                    'id': lesson.id,
                    'title': lesson.title,
                    'content_text': lesson.content_text,
                    'video_url': lesson.video_url,
                    'order_index': lesson.order_index
                } for lesson in section.lessons]
            } for section in course.sections],
            'average_rating': round(float(avg_rating), 1) if avg_rating else 0,
            'rating_count': rating_count or 0,
            'recent_ratings': ratings_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@course_bp.route('/courses/<int:course_id>/rate', methods=['POST'])
@jwt_required()
def rate_course(course_id):
    """Rate a course"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        if 'rating' not in data or not (1 <= data['rating'] <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Check if course exists
        course = Course.query.get_or_404(course_id)
        
        # Check if user already rated this course
        existing_rating = CourseRating.query.filter_by(
            user_id=user_id, 
            course_id=course_id
        ).first()
        
        if existing_rating:
            # Update existing rating
            existing_rating.rating = data['rating']
            existing_rating.review_text = data.get('review_text')
        else:
            # Create new rating
            rating = CourseRating(
                user_id=user_id,
                course_id=course_id,
                rating=data['rating'],
                review_text=data.get('review_text')
            )
            db.session.add(rating)
        
        db.session.commit()
        
        return jsonify({'message': 'Course rated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@course_bp.route('/courses/<int:course_id>/progress', methods=['GET'])
@jwt_required()
def get_course_progress(course_id):
    """Get user's progress in a course"""
    try:
        user_id = get_jwt_identity()
        
        progress = UserCourseProgress.query.filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()
        
        if not progress:
            return jsonify({
                'status': 'not_started',
                'completed_lessons': [],
                'started_at': None,
                'completed_at': None
            }), 200
        
        return jsonify({
            'status': progress.status,
            'completed_lessons': progress.completed_lessons or [],
            'started_at': progress.started_at.isoformat() if progress.started_at else None,
            'completed_at': progress.completed_at.isoformat() if progress.completed_at else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@course_bp.route('/courses/<int:course_id>/progress', methods=['POST'])
@jwt_required()
def update_course_progress(course_id):
    """Update user's progress in a course"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        # Check if course exists
        course = Course.query.get_or_404(course_id)
        
        # Get or create progress record
        progress = UserCourseProgress.query.filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()
        
        if not progress:
            progress = UserCourseProgress(
                user_id=user_id,
                course_id=course_id,
                completed_lessons=[]
            )
            db.session.add(progress)
        
        # Update progress
        if 'lesson_id' in data:
            progress.lesson_id = data['lesson_id']
        
        if 'completed_lessons' in data:
            progress.completed_lessons = data['completed_lessons']
        
        if 'status' in data:
            progress.status = data['status']
            if data['status'] == 'completed':
                progress.completed_at = db.func.now()
        
        db.session.commit()
        
        return jsonify({'message': 'Progress updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@course_bp.route('/courses/featured', methods=['GET'])
def get_featured_courses():
    """Get featured courses (highest rated)"""
    try:
        # Get courses with highest average ratings
        featured_courses = db.session.query(
            Course,
            func.avg(CourseRating.rating).label('avg_rating'),
            func.count(CourseRating.id).label('rating_count')
        ).outerjoin(CourseRating).group_by(Course.id).having(
            func.count(CourseRating.id) >= 5  # At least 5 ratings
        ).order_by(func.avg(CourseRating.rating).desc()).limit(6).all()
        
        course_list = []
        for course, avg_rating, rating_count in featured_courses:
            course_list.append({
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'youtube_video_id': course.youtube_video_id,
                'language': course.language,
                'level': course.level,
                'programming_language': course.programming_language,
                'instructor_name': course.instructor_name,
                'average_rating': round(float(avg_rating), 1) if avg_rating else 0,
                'rating_count': rating_count or 0
            })
        
        return jsonify({'featured_courses': course_list}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

