from flask import Blueprint, jsonify, request
from src.models.database import db, Game, UserGameScore
from flask_jwt_extended import jwt_required, get_jwt_identity

game_bp = Blueprint('game', __name__, url_prefix='/api/games')

@game_bp.route('', methods=['GET'])
def get_all_games():
    """Get all games"""
    games = Game.query.all()
    
    # Format response
    result = {
        'games': [
            {
                'id': game.id,
                'title': game.title,
                'description': game.description,
                'game_url': game.game_url,
                'created_at': game.created_at.isoformat()
            } for game in games
        ]
    }
    
    return jsonify(result)

@game_bp.route('/<int:game_id>', methods=['GET'])
def get_game(game_id):
    """Get a specific game by ID"""
    game = Game.query.get_or_404(game_id)
    
    # Get top scores
    top_scores = UserGameScore.query.filter_by(game_id=game_id).order_by(UserGameScore.score.desc()).limit(10).all()
    
    # Format response
    result = {
        'id': game.id,
        'title': game.title,
        'description': game.description,
        'game_url': game.game_url,
        'created_at': game.created_at.isoformat(),
        'top_scores': [
            {
                'user_id': score.user_id,
                'username': score.user.username,
                'score': score.score,
                'played_at': score.played_at.isoformat()
            } for score in top_scores
        ]
    }
    
    return jsonify(result)

@game_bp.route('/<int:game_id>/score', methods=['POST'])
@jwt_required()
def submit_score(game_id):
    """Submit a score for a game"""
    user_id = get_jwt_identity()
    
    # Check if game exists
    game = Game.query.get_or_404(game_id)
    
    # Get score from request
    data = request.get_json()
    if not data or 'score' not in data:
        return jsonify({'message': 'Score is required'}), 400
    
    score = data.get('score')
    if not isinstance(score, int) or score < 0:
        return jsonify({'message': 'Score must be a positive integer'}), 400
    
    # Check if user already has a score for this game
    user_score = UserGameScore.query.filter_by(user_id=user_id, game_id=game_id).first()
    
    if user_score:
        # Update score if new score is higher
        if score > user_score.score:
            user_score.score = score
            db.session.commit()
            return jsonify({'message': 'Score updated successfully', 'score': score})
        else:
            return jsonify({'message': 'Your previous score was higher', 'score': user_score.score})
    else:
        # Create new score
        new_score = UserGameScore(user_id=user_id, game_id=game_id, score=score)
        db.session.add(new_score)
        db.session.commit()
        return jsonify({'message': 'Score submitted successfully', 'score': score})

@game_bp.route('/<int:game_id>/leaderboard', methods=['GET'])
def get_leaderboard(game_id):
    """Get leaderboard for a game"""
    # Check if game exists
    game = Game.query.get_or_404(game_id)
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # Get scores
    scores_query = UserGameScore.query.filter_by(game_id=game_id).order_by(UserGameScore.score.desc())
    
    # Apply pagination
    pagination = scores_query.paginate(page=page, per_page=limit, error_out=False)
    scores = pagination.items
    
    # Format response
    result = {
        'game': {
            'id': game.id,
            'title': game.title
        },
        'leaderboard': [
            {
                'rank': (page - 1) * limit + i + 1,
                'user_id': score.user_id,
                'username': score.user.username,
                'score': score.score,
                'played_at': score.played_at.isoformat()
            } for i, score in enumerate(scores)
        ],
        'page': page,
        'limit': limit,
        'total': pagination.total,
        'pages': pagination.pages
    }
    
    return jsonify(result)

