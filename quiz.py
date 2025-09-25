from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, Quiz, QuizQuestion, UserQuizAttempt
from sqlalchemy import func

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quizzes', methods=['GET'])
def get_quizzes():
    """Get all quizzes with filters"""
    try:
        # Get query parameters
        programming_language = request.args.get('programming_language')
        level = request.args.get('level')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        query = Quiz.query
        
        if programming_language:
            query = query.filter(Quiz.programming_language == programming_language)
        if level:
            query = query.filter(Quiz.level == level)
        
        # Paginate
        quizzes = query.paginate(page=page, per_page=per_page, error_out=False)
        
        quiz_list = []
        for quiz in quizzes.items:
            # Get attempt count
            attempt_count = db.session.query(func.count(UserQuizAttempt.id)).filter(
                UserQuizAttempt.quiz_id == quiz.id
            ).scalar()
            
            quiz_list.append({
                'id': quiz.id,
                'title': quiz.title,
                'description': quiz.description,
                'programming_language': quiz.programming_language,
                'level': quiz.level,
                'question_count': quiz.question_count,
                'time_limit_minutes': quiz.time_limit_minutes,
                'created_at': quiz.created_at.isoformat() if quiz.created_at else None,
                'attempt_count': attempt_count or 0
            })
        
        return jsonify({
            'quizzes': quiz_list,
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

@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get quiz details (without answers)"""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        
        # Get questions without correct answers
        questions = []
        for question in quiz.questions:
            question_data = {
                'id': question.id,
                'question_text': question.question_text,
                'question_type': question.question_type,
                'code_snippet': question.code_snippet,
                'options': question.options,
                'difficulty_points': question.difficulty_points
            }
            questions.append(question_data)
        
        return jsonify({
            'id': quiz.id,
            'title': quiz.title,
            'description': quiz.description,
            'programming_language': quiz.programming_language,
            'level': quiz.level,
            'question_count': quiz.question_count,
            'time_limit_minutes': quiz.time_limit_minutes,
            'created_at': quiz.created_at.isoformat() if quiz.created_at else None,
            'questions': questions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id):
    """Submit quiz answers"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        if 'answers' not in data:
            return jsonify({'error': 'No answers provided'}), 400
        
        # Get quiz
        quiz = Quiz.query.get_or_404(quiz_id)
        
        # Calculate score
        score = 0
        answers = data['answers']
        
        for answer in answers:
            question_id = answer.get('question_id')
            user_answer = answer.get('answer')
            
            if not question_id or user_answer is None:
                continue
            
            question = QuizQuestion.query.get(question_id)
            if not question or question.quiz_id != quiz_id:
                continue
            
            # Check answer
            if question.question_type == 'multiple_choice':
                if str(user_answer) == str(question.correct_answer):
                    score += question.difficulty_points
            elif question.question_type in ['code_output', 'code_completion', 'debugging']:
                # For code questions, we might need more sophisticated comparison
                # For now, just do a simple string comparison
                if str(user_answer).strip() == str(question.correct_answer).strip():
                    score += question.difficulty_points
        
        # Create attempt record
        attempt = UserQuizAttempt(
            user_id=user_id,
            quiz_id=quiz_id,
            score=score,
            answers_submitted=answers
        )
        db.session.add(attempt)
        db.session.commit()
        
        # Get correct answers for feedback
        correct_answers = {}
        for question in quiz.questions:
            correct_answers[question.id] = {
                'correct_answer': question.correct_answer,
                'explanation': question.explanation
            }
        
        return jsonify({
            'message': 'Quiz submitted successfully',
            'score': score,
            'total_possible': sum(q.difficulty_points for q in quiz.questions),
            'correct_answers': correct_answers,
            'attempt_id': attempt.id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/quizzes/user/attempts', methods=['GET'])
@jwt_required()
def get_user_quiz_attempts():
    """Get user's quiz attempts"""
    try:
        user_id = get_jwt_identity()
        
        attempts = UserQuizAttempt.query.filter_by(user_id=user_id).order_by(
            UserQuizAttempt.attempt_date.desc()
        ).all()
        
        attempt_list = []
        for attempt in attempts:
            attempt_list.append({
                'id': attempt.id,
                'quiz_id': attempt.quiz_id,
                'quiz_title': attempt.quiz.title,
                'score': attempt.score,
                'total_possible': sum(q.difficulty_points for q in attempt.quiz.questions),
                'attempt_date': attempt.attempt_date.isoformat() if attempt.attempt_date else None
            })
        
        return jsonify({
            'attempts': attempt_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/quizzes/leaderboard', methods=['GET'])
def get_quiz_leaderboard():
    """Get quiz leaderboard"""
    try:
        quiz_id = request.args.get('quiz_id')
        limit = int(request.args.get('limit', 10))
        
        # Build query
        query = db.session.query(
            UserQuizAttempt,
            func.max(UserQuizAttempt.score).label('best_score')
        ).join(UserQuizAttempt.user)
        
        if quiz_id:
            query = query.filter(UserQuizAttempt.quiz_id == quiz_id)
        
        # Group by user and get best score
        query = query.group_by(UserQuizAttempt.user_id)
        
        # Order by best score
        query = query.order_by(func.max(UserQuizAttempt.score).desc())
        
        # Limit results
        query = query.limit(limit)
        
        results = query.all()
        
        leaderboard = []
        for attempt, best_score in results:
            leaderboard.append({
                'user_id': attempt.user_id,
                'username': attempt.user.username,
                'profile_picture_url': attempt.user.profile_picture_url,
                'score': best_score,
                'quiz_id': attempt.quiz_id if quiz_id else None,
                'quiz_title': attempt.quiz.title if quiz_id else None
            })
        
        return jsonify({
            'leaderboard': leaderboard
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

