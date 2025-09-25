import os
import sys
import datetime
import random
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask import Flask
from src.models.database import db, Game, AITool, Forum, ForumPost
from src.models.database import UserGameScore, UserCourseProgress, Comment

def create_app():
    """Create Flask app for seeding data"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 
        f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'code_aura_dev.db')}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    return app

def seed_games():
    """Seed games data"""
    print("Seeding games...")
    
    games = [
        {
            "title": "Code Breaker",
            "description": "لعبة تحدي برمجية تختبر مهاراتك في حل المشكلات البرمجية. عليك فك شفرة الكود وإصلاح الأخطاء في وقت محدد.",
            "game_url": "https://example.com/games/code-breaker"
        },
        {
            "title": "Python Quest",
            "description": "مغامرة تعليمية تأخذك في رحلة لتعلم Python من خلال حل الألغاز وإكمال التحديات البرمجية.",
            "game_url": "https://example.com/games/python-quest"
        },
        {
            "title": "CSS Battle",
            "description": "تحدي تصميم يختبر مهاراتك في CSS. عليك إعادة إنشاء التصميم المعروض باستخدام أقل عدد ممكن من أكواد CSS.",
            "game_url": "https://example.com/games/css-battle"
        },
        {
            "title": "Algorithm Adventure",
            "description": "لعبة مغامرة تعليمية تركز على الخوارزميات وهياكل البيانات. تعلم وطبق مفاهيم مثل البحث والفرز وحل المشكلات.",
            "game_url": "https://example.com/games/algorithm-adventure"
        },
        {
            "title": "SQL Island",
            "description": "مغامرة تفاعلية لتعلم SQL. أنت عالق على جزيرة وعليك استخدام استعلامات SQL للتفاعل مع سكان الجزيرة والهروب.",
            "game_url": "https://example.com/games/sql-island"
        }
    ]
    
    for game_data in games:
        game = Game(**game_data)
        db.session.add(game)
    
    db.session.commit()
    print(f"Added {len(games)} games")

def seed_ai_tools():
    """Seed AI tools data"""
    print("Seeding AI tools...")
    
    ai_tools = [
        {
            "name": "Code Companion",
            "description": "مساعد برمجة ذكي يقترح أكواداً أثناء الكتابة ويساعد في إكمال الكود بناءً على السياق.",
            "api_endpoint": "/api/ai-tools/code-companion",
            "tool_type": "generate_code"
        },
        {
            "name": "Bug Hunter",
            "description": "أداة تحليل أكواد تكتشف الأخطاء البرمجية وتقترح إصلاحات لها.",
            "api_endpoint": "/api/ai-tools/bug-hunter",
            "tool_type": "debug_code"
        },
        {
            "name": "Code Translator",
            "description": "أداة لترجمة الكود بين لغات البرمجة المختلفة مع الحفاظ على الوظائف.",
            "api_endpoint": "/api/ai-tools/code-translator",
            "tool_type": "convert_code"
        },
        {
            "name": "Code Explainer",
            "description": "أداة تشرح الكود بلغة بسيطة وتوضح كيفية عمله خطوة بخطوة.",
            "api_endpoint": "/api/ai-tools/code-explainer",
            "tool_type": "explain_code"
        },
        {
            "name": "Code Optimizer",
            "description": "أداة تحسين الكود لزيادة الأداء وتقليل استهلاك الموارد.",
            "api_endpoint": "/api/ai-tools/code-optimizer",
            "tool_type": "debug_code"
        }
    ]
    
    for tool_data in ai_tools:
        tool = AITool(**tool_data)
        db.session.add(tool)
    
    db.session.commit()
    print(f"Added {len(ai_tools)} AI tools")

def seed_forums():
    """Seed forums data"""
    print("Seeding forums...")
    
    forums = [
        {
            "name": "منتدى المبتدئين",
            "description": "منتدى مخصص للمبتدئين في عالم البرمجة لطرح الأسئلة والحصول على المساعدة.",
            "category_id": 10
        },
        {
            "name": "تطوير الويب",
            "description": "نقاشات حول تطوير مواقع الويب، HTML، CSS، JavaScript، وأطر العمل المختلفة.",
            "category_id": 2
        },
        {
            "name": "تطوير تطبيقات الموبايل",
            "description": "منتدى لمناقشة تطوير تطبيقات الهواتف الذكية لنظامي Android و iOS.",
            "category_id": 3
        },
        {
            "name": "قواعد البيانات",
            "description": "نقاشات حول قواعد البيانات، SQL، NoSQL، وتصميم قواعد البيانات.",
            "category_id": 4
        },
        {
            "name": "الذكاء الاصطناعي وتعلم الآلة",
            "description": "منتدى لمناقشة مواضيع الذكاء الاصطناعي، تعلم الآلة، والتعلم العميق.",
            "category_id": 5
        }
    ]
    
    for forum_data in forums:
        forum = Forum(**forum_data)
        db.session.add(forum)
    
    db.session.commit()
    
    # Add some forum posts
    forum_posts = [
        {
            "forum_id": 1,
            "user_id": 3,
            "title": "كيف أبدأ تعلم البرمجة؟",
            "content": "أنا مبتدئ تماماً في عالم البرمجة وأريد أن أبدأ التعلم. ما هي اللغة الأفضل للبدء بها؟ وما هي الموارد التي تنصحون بها؟",
            "parent_post_id": None
        },
        {
            "forum_id": 1,
            "user_id": 2,
            "title": "رد: كيف أبدأ تعلم البرمجة؟",
            "content": "أنصحك بالبدء بلغة Python لأنها سهلة التعلم ومناسبة للمبتدئين. يمكنك البدء بدورة 'البرمجة بلغة Python للمبتدئين' على منصتنا.",
            "parent_post_id": 1
        },
        {
            "forum_id": 2,
            "user_id": 4,
            "title": "ما هو أفضل إطار عمل لتطوير الواجهات الأمامية؟",
            "content": "أنا محتار بين React و Vue و Angular. ما هو الإطار الأفضل للمشاريع المتوسطة الحجم؟",
            "parent_post_id": None
        },
        {
            "forum_id": 3,
            "user_id": 5,
            "title": "مقارنة بين Flutter و React Native",
            "content": "أريد أن أبدأ في تطوير تطبيقات الموبايل. هل تنصحون باستخدام Flutter أم React Native؟ ما هي مزايا وعيوب كل منهما؟",
            "parent_post_id": None
        },
        {
            "forum_id": 5,
            "user_id": 1,
            "title": "كيفية البدء في مشاريع الذكاء الاصطناعي",
            "content": "أنا مهتم بالذكاء الاصطناعي وأريد أن أبدأ في تطوير مشاريع بسيطة. ما هي المكتبات والأدوات التي تنصحون بها للمبتدئين؟",
            "parent_post_id": None
        }
    ]
    
    for post_data in forum_posts:
        post = ForumPost(**post_data)
        db.session.add(post)
    
    db.session.commit()
    print(f"Added {len(forums)} forums and {len(forum_posts)} forum posts")

def seed_game_scores():
    """Seed game scores data"""
    print("Seeding game scores...")
    
    # Game scores
    for i in range(1, 6):  # For each game
        num_scores = random.randint(3, 10)
        for j in range(num_scores):
            user_id = random.randint(1, 6)  # Random user
            score = random.randint(50, 100)  # Score between 50-100
            
            # Check if score already exists
            existing_score = UserGameScore.query.filter_by(user_id=user_id, game_id=i).first()
            if not existing_score:
                game_score = UserGameScore(
                    user_id=user_id,
                    game_id=i,
                    score=score
                )
                db.session.add(game_score)
    
    db.session.commit()
    print("Added game scores data")

def main():
    """Main function to seed remaining data"""
    app = create_app()
    
    with app.app_context():
        # Seed data
        seed_games()
        seed_ai_tools()
        seed_forums()
        seed_game_scores()
        
        print("Remaining data seeding completed successfully!")

if __name__ == "__main__":
    main()

