from flask import Blueprint, jsonify, request
from src.models.database import db, Article, Category
from flask_jwt_extended import jwt_required, get_jwt_identity

article_bp = Blueprint('article', __name__, url_prefix='/api/articles')

@article_bp.route('', methods=['GET'])
def get_all_articles():
    """Get all published articles with pagination"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # Get articles query
    query = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc())
    
    # Apply pagination
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    articles = pagination.items
    
    # Format response
    result = {
        'articles': [
            {
                'id': article.id,
                'title': article.title,
                'content': article.content[:200] + '...' if len(article.content) > 200 else article.content,
                'author_id': article.author_id,
                'created_at': article.created_at.isoformat(),
                'is_published': article.is_published
            } for article in articles
        ],
        'page': page,
        'limit': limit,
        'total': pagination.total,
        'pages': pagination.pages
    }
    
    return jsonify(result)

@article_bp.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """Get a specific article by ID"""
    article = Article.query.get_or_404(article_id)
    
    # Check if article is published or user is the author
    if not article.is_published:
        return jsonify({'message': 'Article not found'}), 404
    
    # Get categories
    categories = []
    for category in article.categories:
        categories.append({
            'id': category.id,
            'name': category.name
        })
    
    # Format response
    result = {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'author_id': article.author_id,
        'author_name': article.author.username if article.author else 'Unknown',
        'created_at': article.created_at.isoformat(),
        'is_published': article.is_published,
        'categories': categories
    }
    
    return jsonify(result)

@article_bp.route('/category/<int:category_id>', methods=['GET'])
def get_articles_by_category(category_id):
    """Get articles by category"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # Check if category exists
    category = Category.query.get_or_404(category_id)
    
    # Get articles for this category
    articles = category.articles.filter_by(is_published=True).order_by(Article.created_at.desc())
    
    # Apply pagination
    pagination = articles.paginate(page=page, per_page=limit, error_out=False)
    articles = pagination.items
    
    # Format response
    result = {
        'category': {
            'id': category.id,
            'name': category.name,
            'description': category.description
        },
        'articles': [
            {
                'id': article.id,
                'title': article.title,
                'content': article.content[:200] + '...' if len(article.content) > 200 else article.content,
                'author_id': article.author_id,
                'created_at': article.created_at.isoformat(),
                'is_published': article.is_published
            } for article in articles
        ],
        'page': page,
        'limit': limit,
        'total': pagination.total,
        'pages': pagination.pages
    }
    
    return jsonify(result)

@article_bp.route('/search', methods=['GET'])
def search_articles():
    """Search articles by query"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    if not query:
        return jsonify({'message': 'Search query is required'}), 400
    
    # Search articles
    search_query = f"%{query}%"
    articles_query = Article.query.filter(
        Article.is_published == True,
        (Article.title.ilike(search_query) | Article.content.ilike(search_query))
    ).order_by(Article.created_at.desc())
    
    # Apply pagination
    pagination = articles_query.paginate(page=page, per_page=limit, error_out=False)
    articles = pagination.items
    
    # Format response
    result = {
        'articles': [
            {
                'id': article.id,
                'title': article.title,
                'content': article.content[:200] + '...' if len(article.content) > 200 else article.content,
                'author_id': article.author_id,
                'created_at': article.created_at.isoformat(),
                'is_published': article.is_published
            } for article in articles
        ],
        'page': page,
        'limit': limit,
        'total': pagination.total,
        'pages': pagination.pages,
        'query': query
    }
    
    return jsonify(result)

