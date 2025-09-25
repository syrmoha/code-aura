import os
import sys
import datetime
import random
import json
from werkzeug.security import generate_password_hash

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask import Flask
from src.models.database import db, User, Course, CourseSection, CourseLesson
from src.models.database import Quiz, QuizQuestion, Article, Game, AITool, Category
from src.models.database import CourseCategory, ArticleCategory, CourseRating, UserQuizAttempt
from src.models.database import Forum, ForumPost, Comment, UserGameScore, UserCourseProgress

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

def seed_categories():
    """Seed categories data"""
    print("Seeding categories...")
    
    categories = [
        {"name": "لغات البرمجة", "description": "دورات وموارد متعلقة بلغات البرمجة المختلفة"},
        {"name": "تطوير الويب", "description": "دورات وموارد متعلقة بتطوير مواقع الويب"},
        {"name": "تطوير الموبايل", "description": "دورات وموارد متعلقة بتطوير تطبيقات الهواتف الذكية"},
        {"name": "قواعد البيانات", "description": "دورات وموارد متعلقة بقواعد البيانات وإدارتها"},
        {"name": "الذكاء الاصطناعي", "description": "دورات وموارد متعلقة بالذكاء الاصطناعي وتعلم الآلة"},
        {"name": "أمن المعلومات", "description": "دورات وموارد متعلقة بأمن المعلومات والحماية السيبرانية"},
        {"name": "تطوير الألعاب", "description": "دورات وموارد متعلقة بتطوير الألعاب الإلكترونية"},
        {"name": "الحوسبة السحابية", "description": "دورات وموارد متعلقة بالحوسبة السحابية وخدماتها"},
        {"name": "DevOps", "description": "دورات وموارد متعلقة بممارسات DevOps وأدواتها"},
        {"name": "البرمجة للمبتدئين", "description": "دورات وموارد مخصصة للمبتدئين في عالم البرمجة"}
    ]
    
    for category_data in categories:
        category = Category(**category_data)
        db.session.add(category)
    
    db.session.commit()
    print(f"Added {len(categories)} categories")

def seed_users():
    """Seed users data"""
    print("Seeding users...")
    
    # Regular users
    users = [
        {
            "username": "ahmed_mohamed",
            "email": "ahmed@example.com",
            "password": "P@ssw0rd123",
            "bio": "مطور ويب متحمس ومهتم بتعلم تقنيات جديدة",
            "profile_picture_url": "https://randomuser.me/api/portraits/men/32.jpg",
            "role": "user"
        },
        {
            "username": "sara_ahmed",
            "email": "sara@example.com",
            "password": "P@ssw0rd123",
            "bio": "مهندسة برمجيات ومدربة في مجال تطوير الويب",
            "profile_picture_url": "https://randomuser.me/api/portraits/women/44.jpg",
            "role": "user"
        },
        {
            "username": "mohamed_ali",
            "email": "mohamed@example.com",
            "password": "P@ssw0rd123",
            "bio": "مطور تطبيقات موبايل باستخدام Flutter",
            "profile_picture_url": "https://randomuser.me/api/portraits/men/22.jpg",
            "role": "user"
        },
        {
            "username": "nora_ahmed",
            "email": "nora@example.com",
            "password": "P@ssw0rd123",
            "bio": "مهتمة بالذكاء الاصطناعي وتعلم الآلة",
            "profile_picture_url": "https://randomuser.me/api/portraits/women/29.jpg",
            "role": "user"
        },
        {
            "username": "omar_hassan",
            "email": "omar@example.com",
            "password": "P@ssw0rd123",
            "bio": "مدير تقني ومهتم بتطوير مهارات فريقي",
            "profile_picture_url": "https://randomuser.me/api/portraits/men/42.jpg",
            "role": "user"
        }
    ]
    
    # Admin user (already created in create_admin.py)
    admin_user = {
        "username": "admin",
        "email": "qaseemmohammad60@gmail.com",
        "password": "Mohammadabukashreef1#$",
        "bio": "مدير منصة Code Aura",
        "profile_picture_url": "https://randomuser.me/api/portraits/men/1.jpg",
        "role": "admin"
    }
    
    # Check if admin exists
    existing_admin = User.query.filter_by(email=admin_user["email"]).first()
    if not existing_admin:
        admin = User(
            username=admin_user["username"],
            email=admin_user["email"],
            password_hash=generate_password_hash(admin_user["password"]),
            bio=admin_user["bio"],
            profile_picture_url=admin_user["profile_picture_url"],
            role=admin_user["role"],
            created_at=datetime.datetime.utcnow(),
            last_login=datetime.datetime.utcnow()
        )
        db.session.add(admin)
    
    # Add regular users
    for user_data in users:
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if not existing_user:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=generate_password_hash(user_data["password"]),
                bio=user_data["bio"],
                profile_picture_url=user_data["profile_picture_url"],
                role=user_data["role"],
                created_at=datetime.datetime.utcnow(),
                last_login=datetime.datetime.utcnow()
            )
            db.session.add(user)
    
    db.session.commit()
    print(f"Added {len(users) + (0 if existing_admin else 1)} users")

def seed_courses():
    """Seed courses data"""
    print("Seeding courses...")
    
    # Arabic courses
    arabic_courses = [
        {
            "title": "البرمجة بلغة Python للمبتدئين",
            "description": "دورة شاملة لتعلم أساسيات البرمجة باستخدام لغة Python. تبدأ من الصفر وتغطي المفاهيم الأساسية مثل المتغيرات، الشروط، الحلقات، الدوال، والتعامل مع الملفات.",
            "youtube_video_id": "rfscVS0vtbw",
            "youtube_playlist_id": "PLDoPjvoNmBAyE_gei5d18qkfIe-Z8mocs",
            "language": "arabic",
            "level": "beginner",
            "programming_language": "Python",
            "duration_minutes": 720,
            "instructor_name": "أحمد محمد",
            "category_ids": [1, 10]
        },
        {
            "title": "تطوير واجهات المستخدم باستخدام React",
            "description": "تعلم كيفية بناء واجهات مستخدم تفاعلية باستخدام مكتبة React. ستتعلم المفاهيم الأساسية مثل المكونات، الحالة، الخصائص، وإدارة الحالة المتقدمة.",
            "youtube_video_id": "w7ejDZ8SWv8",
            "youtube_playlist_id": "PLDoPjvoNmBAy1l-2A21ng3gxEyocruT0t",
            "language": "arabic",
            "level": "intermediate",
            "programming_language": "JavaScript",
            "duration_minutes": 900,
            "instructor_name": "سارة أحمد",
            "category_ids": [1, 2]
        },
        {
            "title": "تطوير تطبيقات الموبايل باستخدام Flutter",
            "description": "دورة شاملة لتعلم تطوير تطبيقات الموبايل لنظامي Android و iOS باستخدام إطار عمل Flutter. ستتعلم كيفية بناء واجهات مستخدم جذابة وتطبيقات متكاملة.",
            "youtube_video_id": "1ukSR1GRtMU",
            "youtube_playlist_id": "PLDoPjvoNmBAzlpyFHOaB3b-eubmF0TAV2",
            "language": "arabic",
            "level": "intermediate",
            "programming_language": "Dart",
            "duration_minutes": 1080,
            "instructor_name": "محمد علي",
            "category_ids": [1, 3]
        },
        {
            "title": "أساسيات قواعد البيانات SQL",
            "description": "تعلم أساسيات قواعد البيانات العلائقية ولغة SQL. ستتعلم كيفية إنشاء الجداول، إدخال البيانات، الاستعلامات، والعلاقات بين الجداول.",
            "youtube_video_id": "HXV3zeQKqGY",
            "youtube_playlist_id": "PLDoPjvoNmBAz6DT8SzQ1CODJTH-NIA7R9",
            "language": "arabic",
            "level": "beginner",
            "programming_language": "SQL",
            "duration_minutes": 600,
            "instructor_name": "فاطمة حسن",
            "category_ids": [4]
        },
        {
            "title": "تعلم JavaScript من الصفر إلى الاحتراف",
            "description": "دورة شاملة لتعلم لغة JavaScript من البداية وحتى المستويات المتقدمة. تغطي الدورة أساسيات اللغة، DOM، الأحداث، AJAX، والمفاهيم المتقدمة.",
            "youtube_video_id": "PkZNo7MFNFg",
            "youtube_playlist_id": "PLDoPjvoNmBAx3kiplQR_oeDqLDBUDYwVv",
            "language": "arabic",
            "level": "beginner",
            "programming_language": "JavaScript",
            "duration_minutes": 1200,
            "instructor_name": "خالد عمر",
            "category_ids": [1, 2]
        },
        {
            "title": "تطوير الويب الكامل - Full Stack Development",
            "description": "تعلم تطوير الويب الكامل باستخدام Node.js و Express و MongoDB للباك إند و React للفرونت إند. ستبني مشاريع متكاملة من البداية إلى النهاية.",
            "youtube_video_id": "nu_pCVPKzTk",
            "youtube_playlist_id": "PLDoPjvoNmBAz9sluuyOWPifXvySgrGma8",
            "language": "arabic",
            "level": "advanced",
            "programming_language": "JavaScript",
            "duration_minutes": 1800,
            "instructor_name": "عمر خالد",
            "category_ids": [1, 2]
        },
        {
            "title": "مقدمة في الذكاء الاصطناعي وتعلم الآلة",
            "description": "دورة تمهيدية في الذكاء الاصطناعي وتعلم الآلة. ستتعلم المفاهيم الأساسية، الخوارزميات، وكيفية بناء نماذج بسيطة باستخدام Python.",
            "youtube_video_id": "JcI5Vnw0b2c",
            "youtube_playlist_id": "PLDoPjvoNmBAy4mM4YjKl0zWEoQHo6Qe8x",
            "language": "arabic",
            "level": "intermediate",
            "programming_language": "Python",
            "duration_minutes": 960,
            "instructor_name": "ليلى أحمد",
            "category_ids": [1, 5]
        },
        {
            "title": "تطوير تطبيقات الويب باستخدام Node.js",
            "description": "تعلم كيفية بناء تطبيقات ويب قوية باستخدام Node.js و Express. ستتعلم كيفية إنشاء API، التعامل مع قواعد البيانات، والمصادقة.",
            "youtube_video_id": "Oe421EPjeBE",
            "youtube_playlist_id": "PLDoPjvoNmBAyE_gei5d18qkfIe-Z8mocs",
            "language": "arabic",
            "level": "intermediate",
            "programming_language": "JavaScript",
            "duration_minutes": 840,
            "instructor_name": "يوسف محمد",
            "category_ids": [1, 2]
        },
        {
            "title": "أساسيات Git و GitHub",
            "description": "تعلم أساسيات نظام التحكم بالإصدارات Git وكيفية استخدام منصة GitHub. ستتعلم الأوامر الأساسية، العمل مع الفروع، وإدارة المشاريع.",
            "youtube_video_id": "RGOj5yH7evk",
            "youtube_playlist_id": "PLDoPjvoNmBAw4eOj58MZPakHjaO3frVMF",
            "language": "arabic",
            "level": "beginner",
            "programming_language": "Git",
            "duration_minutes": 480,
            "instructor_name": "أحمد سمير",
            "category_ids": [1, 9]
        },
        {
            "title": "تطوير تطبيقات الويب التفاعلية باستخدام Vue.js",
            "description": "تعلم كيفية بناء تطبيقات ويب تفاعلية باستخدام إطار عمل Vue.js. ستتعلم المكونات، إدارة الحالة، والتوجيه.",
            "youtube_video_id": "qZXt1Aom3Cs",
            "youtube_playlist_id": "PLDoPjvoNmBAzDuaT7kEURZQbw9dQHepK9",
            "language": "arabic",
            "level": "intermediate",
            "programming_language": "JavaScript",
            "duration_minutes": 720,
            "instructor_name": "نورا محمد",
            "category_ids": [1, 2]
        }
    ]
    
    # English courses
    english_courses = [
        {
            "title": "Python for Beginners",
            "description": "A comprehensive course to learn Python programming from scratch. Covers basic concepts like variables, conditionals, loops, functions, and file handling.",
            "youtube_video_id": "rfscVS0vtbw",
            "youtube_playlist_id": "PLlrxD0HtieHhS8VzuMCfQD4uJ9yne1mE6",
            "language": "english",
            "level": "beginner",
            "programming_language": "Python",
            "duration_minutes": 720,
            "instructor_name": "John Smith",
            "category_ids": [1, 10]
        },
        {
            "title": "React.js Crash Course",
            "description": "Learn how to build interactive user interfaces using React.js. You'll learn core concepts like components, state, props, and advanced state management.",
            "youtube_video_id": "w7ejDZ8SWv8",
            "youtube_playlist_id": "PLillGF-RfqbY3c2r0htQyVbDJJoBFE6Rb",
            "language": "english",
            "level": "intermediate",
            "programming_language": "JavaScript",
            "duration_minutes": 900,
            "instructor_name": "Sarah Johnson",
            "category_ids": [1, 2]
        },
        {
            "title": "Flutter Mobile App Development",
            "description": "A comprehensive course on developing mobile applications for Android and iOS using Flutter framework. Learn to build attractive UIs and complete applications.",
            "youtube_video_id": "1ukSR1GRtMU",
            "youtube_playlist_id": "PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG",
            "language": "english",
            "level": "intermediate",
            "programming_language": "Dart",
            "duration_minutes": 1080,
            "instructor_name": "Michael Brown",
            "category_ids": [1, 3]
        }
    ]
    
    # Combine courses
    all_courses = arabic_courses + english_courses
    
    for course_data in all_courses:
        # Extract category IDs
        category_ids = course_data.pop('category_ids', [])
        
        # Create course
        course = Course(**course_data)
        db.session.add(course)
        db.session.flush()  # Get course ID
        
        # Add categories
        for category_id in category_ids:
            course_category = CourseCategory(course_id=course.id, category_id=category_id)
            db.session.add(course_category)
        
        # Add sections and lessons
        num_sections = random.randint(3, 8)
        for i in range(1, num_sections + 1):
            section = CourseSection(
                course_id=course.id,
                title=f"القسم {i}: {generate_section_title(course_data['programming_language'], i)}",
                order=i,
                description=f"وصف للقسم {i} من الدورة"
            )
            db.session.add(section)
            db.session.flush()  # Get section ID
            
            num_lessons = random.randint(3, 7)
            for j in range(1, num_lessons + 1):
                lesson = CourseLesson(
                    section_id=section.id,
                    title=f"الدرس {j}: {generate_lesson_title(course_data['programming_language'], i, j)}",
                    order=j,
                    content_type="video",
                    content_url=f"https://www.youtube.com/watch?v={course_data['youtube_video_id']}&list={course_data['youtube_playlist_id']}&index={j}",
                    duration_minutes=random.randint(10, 30)
                )
                db.session.add(lesson)
    
    db.session.commit()
    print(f"Added {len(all_courses)} courses with sections and lessons")

def generate_section_title(programming_language, section_number):
    """Generate a section title based on programming language and section number"""
    python_sections = [
        "مقدمة في البرمجة وبيئة Python",
        "المتغيرات وأنواع البيانات",
        "الشروط والتحكم بالمسار",
        "الحلقات التكرارية",
        "الدوال والوحدات",
        "التعامل مع الملفات",
        "البرمجة كائنية التوجه",
        "معالجة الأخطاء والاستثناءات"
    ]
    
    javascript_sections = [
        "مقدمة في JavaScript",
        "المتغيرات والعمليات",
        "الدوال والنطاقات",
        "المصفوفات والكائنات",
        "DOM والتفاعل مع صفحات الويب",
        "الأحداث والتعامل معها",
        "AJAX والتعامل مع البيانات",
        "ES6 والميزات الحديثة"
    ]
    
    react_sections = [
        "مقدمة في React",
        "المكونات والخصائص",
        "الحالة وإدارتها",
        "دورة حياة المكونات",
        "التعامل مع النماذج",
        "التوجيه في React",
        "إدارة الحالة المتقدمة",
        "اختبار تطبيقات React"
    ]
    
    if programming_language == "Python":
        return python_sections[min(section_number - 1, len(python_sections) - 1)]
    elif programming_language == "JavaScript":
        return javascript_sections[min(section_number - 1, len(javascript_sections) - 1)]
    elif programming_language == "React":
        return react_sections[min(section_number - 1, len(react_sections) - 1)]
    else:
        return f"القسم {section_number}"

def generate_lesson_title(programming_language, section_number, lesson_number):
    """Generate a lesson title based on programming language, section and lesson numbers"""
    python_lessons = {
        1: ["تثبيت Python", "بيئة التطوير المتكاملة", "أول برنامج Hello World", "التعليقات والتوثيق"],
        2: ["المتغيرات وتعريفها", "أنواع البيانات الأساسية", "العمليات الحسابية", "تحويل أنواع البيانات"],
        3: ["عبارات if", "العمليات المنطقية", "عبارات if المتداخلة", "عبارة elif"],
        4: ["حلقة for", "حلقة while", "عبارات break و continue", "الحلقات المتداخلة"]
    }
    
    javascript_lessons = {
        1: ["مقدمة في JavaScript", "إضافة JavaScript إلى صفحات الويب", "المتصفح وأدوات المطور", "أول برنامج Hello World"],
        2: ["المتغيرات وتعريفها", "أنواع البيانات", "العمليات الحسابية والمنطقية", "التحويل بين أنواع البيانات"],
        3: ["تعريف الدوال", "المعاملات والقيم المرجعة", "النطاقات", "الدوال السهمية"],
        4: ["المصفوفات وتعريفها", "العمليات على المصفوفات", "الكائنات", "JSON"]
    }
    
    if programming_language == "Python" and section_number in python_lessons:
        lessons = python_lessons[section_number]
        return lessons[min(lesson_number - 1, len(lessons) - 1)]
    elif programming_language == "JavaScript" and section_number in javascript_lessons:
        lessons = javascript_lessons[section_number]
        return lessons[min(lesson_number - 1, len(lessons) - 1)]
    else:
        return f"الدرس {lesson_number}"

def seed_quizzes():
    """Seed quizzes data"""
    print("Seeding quizzes...")
    
    quizzes = [
        {
            "title": "اختبار أساسيات Python",
            "description": "اختبر معرفتك بأساسيات لغة Python من المتغيرات إلى الدوال",
            "programming_language": "Python",
            "level": "beginner",
            "question_count": 10,
            "time_limit_minutes": 20,
            "questions": [
                {
                    "question_text": "ما هي النتيجة المتوقعة لهذا الكود؟\n```python\nx = 5\ny = 2\nprint(x ** y)\n```",
                    "question_type": "multiple_choice",
                    "code_snippet": "x = 5\ny = 2\nprint(x ** y)",
                    "options": ["7", "10", "25", "3"],
                    "correct_answer": "25",
                    "explanation": "العملية ** في Python تعني الأس، لذا x ** y تساوي 5^2 = 25",
                    "difficulty_points": 1
                },
                {
                    "question_text": "ما هو نوع البيانات الناتج عن هذا التعبير؟\n```python\nx = 5 / 2\ntype(x)\n```",
                    "question_type": "multiple_choice",
                    "code_snippet": "x = 5 / 2\ntype(x)",
                    "options": ["int", "float", "double", "decimal"],
                    "correct_answer": "float",
                    "explanation": "عملية القسمة / في Python تنتج دائماً قيمة عشرية (float)",
                    "difficulty_points": 1
                }
            ]
        },
        {
            "title": "اختبار JavaScript المتقدم",
            "description": "اختبر معرفتك بالمفاهيم المتقدمة في JavaScript مثل الدوال السهمية، الوعود، و async/await",
            "programming_language": "JavaScript",
            "level": "advanced",
            "question_count": 10,
            "time_limit_minutes": 30,
            "questions": [
                {
                    "question_text": "ما هي النتيجة المتوقعة لهذا الكود؟\n```javascript\nconst arr = [1, 2, 3, 4, 5];\nconst result = arr.map(x => x * 2).filter(x => x > 5);\nconsole.log(result);\n```",
                    "question_type": "multiple_choice",
                    "code_snippet": "const arr = [1, 2, 3, 4, 5];\nconst result = arr.map(x => x * 2).filter(x => x > 5);\nconsole.log(result);",
                    "options": ["[2, 4, 6, 8, 10]", "[6, 8, 10]", "[3, 4, 5]", "[1, 2, 3, 4, 5]"],
                    "correct_answer": "[6, 8, 10]",
                    "explanation": "أولاً يتم ضرب كل عنصر في 2 باستخدام map لينتج [2, 4, 6, 8, 10]، ثم يتم تصفية العناصر الأكبر من 5 باستخدام filter لينتج [6, 8, 10]",
                    "difficulty_points": 2
                },
                {
                    "question_text": "ما هي النتيجة المتوقعة لهذا الكود؟\n```javascript\nconsole.log(typeof null);\n```",
                    "question_type": "multiple_choice",
                    "code_snippet": "console.log(typeof null);",
                    "options": ["null", "undefined", "object", "number"],
                    "correct_answer": "object",
                    "explanation": "في JavaScript، typeof null يرجع 'object' وهو خطأ تاريخي في اللغة",
                    "difficulty_points": 1
                }
            ]
        },
        {
            "title": "اختبار SQL للمبتدئين",
            "description": "اختبر معرفتك بأساسيات SQL والاستعلامات البسيطة",
            "programming_language": "SQL",
            "level": "beginner",
            "question_count": 10,
            "time_limit_minutes": 15,
            "questions": [
                {
                    "question_text": "أي من الاستعلامات التالية يسترجع جميع الأعمدة من جدول 'users'؟",
                    "question_type": "multiple_choice",
                    "options": ["SELECT users FROM *;", "SELECT * FROM users;", "SELECT ALL FROM users;", "SELECT COLUMNS FROM users;"],
                    "correct_answer": "SELECT * FROM users;",
                    "explanation": "الاستعلام SELECT * FROM users; يسترجع جميع الأعمدة من جدول users",
                    "difficulty_points": 1
                },
                {
                    "question_text": "أي من العبارات التالية تستخدم لإضافة صف جديد إلى جدول 'users'؟",
                    "question_type": "multiple_choice",
                    "options": ["ADD INTO users VALUES (1, 'John');", "INSERT VALUES (1, 'John') INTO users;", "INSERT INTO users VALUES (1, 'John');", "UPDATE users SET VALUES (1, 'John');"],
                    "correct_answer": "INSERT INTO users VALUES (1, 'John');",
                    "explanation": "العبارة INSERT INTO تستخدم لإضافة صفوف جديدة إلى الجدول",
                    "difficulty_points": 1
                }
            ]
        }
    ]
    
    for quiz_data in quizzes:
        # Extract questions
        questions_data = quiz_data.pop('questions', [])
        
        # Create quiz
        quiz = Quiz(**quiz_data)
        db.session.add(quiz)
        db.session.flush()  # Get quiz ID
        
        # Add questions
        for question_data in questions_data:
            question = QuizQuestion(quiz_id=quiz.id, **question_data)
            db.session.add(question)
    
    db.session.commit()
    print(f"Added {len(quizzes)} quizzes with questions")

def seed_articles():
    """Seed articles data"""
    print("Seeding articles...")
    
    articles = [
        {
            "title": "كيف تبدأ رحلتك في عالم البرمجة",
            "content": """# كيف تبدأ رحلتك في عالم البرمجة

## مقدمة

البرمجة هي واحدة من أكثر المهارات طلباً في سوق العمل اليوم. سواء كنت ترغب في تغيير مسارك المهني، أو تطوير مهاراتك الحالية، أو حتى مجرد تعلم شيء جديد، فإن تعلم البرمجة يمكن أن يفتح لك العديد من الأبواب.

في هذا المقال، سنستعرض الخطوات الأساسية التي يمكنك اتباعها لبدء رحلتك في عالم البرمجة، بغض النظر عن خلفيتك أو عمرك.

## حدد هدفك من تعلم البرمجة

قبل أن تبدأ في تعلم البرمجة، من المهم أن تحدد هدفك. هل ترغب في:

- تطوير تطبيقات الويب؟
- إنشاء تطبيقات للهواتف الذكية؟
- العمل في مجال تحليل البيانات والذكاء الاصطناعي؟
- تطوير ألعاب إلكترونية؟
- أتمتة المهام اليومية؟

تحديد هدفك سيساعدك في اختيار لغة البرمجة المناسبة والمسار التعليمي الأفضل لك.

## اختر لغة البرمجة المناسبة للبداية

هناك العديد من لغات البرمجة المتاحة، ولكن ليس عليك تعلمها جميعاً في البداية. إليك بعض الاقتراحات بناءً على اهتماماتك:

- **Python**: لغة سهلة التعلم ومتعددة الاستخدامات، مثالية للمبتدئين وتستخدم في تحليل البيانات والذكاء الاصطناعي وتطوير الويب.
- **JavaScript**: أساسية لتطوير الويب، تستخدم في الواجهات الأمامية والخلفية.
- **Swift/Kotlin**: لتطوير تطبيقات iOS/Android.
- **C#/Unity**: لتطوير الألعاب.
- **SQL**: للتعامل مع قواعد البيانات.

للمبتدئين، غالباً ما يُنصح بالبدء بـ Python نظراً لبساطة بناء الجملة وتعدد استخداماتها.

## استفد من الموارد التعليمية المتاحة

هناك العديد من الموارد المتاحة لتعلم البرمجة، منها:

- **الدورات عبر الإنترنت**: منصات مثل Code Aura، Coursera، edX، Udemy تقدم دورات في مختلف لغات البرمجة.
- **الكتب**: هناك العديد من الكتب المخصصة للمبتدئين في البرمجة.
- **المشاريع العملية**: تطبيق ما تتعلمه من خلال مشاريع صغيرة.
- **المجتمعات**: الانضمام إلى مجتمعات البرمجة مثل Stack Overflow، GitHub، أو المنتديات المتخصصة.

## ابدأ بالأساسيات

تعلم أساسيات البرمجة أولاً، مثل:

- المتغيرات وأنواع البيانات
- الشروط والحلقات
- الدوال والوحدات
- هياكل البيانات الأساسية (المصفوفات، القوائم، القواميس)
- مفاهيم البرمجة كائنية التوجه

## مارس بانتظام

البرمجة مهارة تحتاج إلى ممارسة مستمرة. حاول تخصيص وقت يومي للتعلم والممارسة، حتى لو كان قصيراً.

## ابنِ مشاريع صغيرة

بعد تعلم الأساسيات، ابدأ في بناء مشاريع صغيرة لتطبيق ما تعلمته. يمكن أن تكون:

- آلة حاسبة بسيطة
- تطبيق قائمة المهام
- موقع شخصي بسيط
- لعبة بسيطة مثل "حجر ورقة مقص"

## لا تخف من الأخطاء

الأخطاء جزء طبيعي من عملية التعلم. عندما تواجه خطأً، حاول فهمه وتصحيحه بنفسك قبل البحث عن الحل.

## تعلم من الآخرين

اقرأ أكواد الآخرين وتعلم من أساليبهم. يمكنك استكشاف مشاريع مفتوحة المصدر على GitHub للاطلاع على كيفية كتابة الكود بشكل احترافي.

## استمر في التعلم

عالم البرمجة في تطور مستمر، لذا من المهم مواكبة أحدث التقنيات والأدوات. اشترك في النشرات الإخبارية، تابع المدونات التقنية، وشارك في المؤتمرات والفعاليات.

## خاتمة

تعلم البرمجة رحلة مستمرة وليست وجهة. استمتع بالعملية، واحتفل بإنجازاتك الصغيرة، ولا تقارن نفسك بالآخرين. كل مبرمج بدأ من الصفر، والمثابرة هي المفتاح للنجاح في هذا المجال.

ابدأ اليوم، واستمر في التعلم، وستجد نفسك قادراً على بناء المشاريع التي كنت تحلم بها.""",
            "author_id": 1,
            "is_published": True,
            "category_ids": [1, 10]
        },
        {
            "title": "مقارنة بين أشهر أطر عمل JavaScript: React vs Vue vs Angular",
            "content": """# مقارنة بين أشهر أطر عمل JavaScript: React vs Vue vs Angular

## مقدمة

في عالم تطوير الويب الحديث، أصبحت أطر عمل JavaScript أدوات أساسية لبناء تطبيقات الويب التفاعلية. من بين العديد من الخيارات المتاحة، تبرز ثلاثة أطر عمل كأكثر الأطر شعبية واستخداماً: React، Vue، و Angular.

في هذا المقال، سنقارن بين هذه الأطر الثلاثة من حيث الأداء، سهولة التعلم، المرونة، والاستخدام في المشاريع المختلفة.

## نظرة عامة

### React

React هي مكتبة JavaScript طورتها شركة Facebook في عام 2013. على الرغم من أنها تُصنف تقنياً كمكتبة وليس إطار عمل كامل، إلا أنها غالباً ما تُقارن مع أطر العمل الأخرى نظراً لاستخدامها الواسع في بناء واجهات المستخدم.

**المميزات الرئيسية:**
- Virtual DOM لتحسين الأداء
- مكونات قابلة لإعادة الاستخدام
- تدفق بيانات أحادي الاتجاه
- JSX لكتابة HTML داخل JavaScript

### Vue

Vue.js هو إطار عمل تطويري تدريجي طوره Evan You في عام 2014. يتميز بتصميمه البسيط وسهولة دمجه مع المشاريع الحالية.

**المميزات الرئيسية:**
- نظام قوالب بسيط وفعال
- Virtual DOM
- مكونات أحادية الملف
- تدريجي وسهل الدمج

### Angular

Angular هو إطار عمل شامل طورته Google. النسخة الحالية (Angular 2+) هي إعادة كتابة كاملة للإصدار الأصلي AngularJS.

**المميزات الرئيسية:**
- نظام شامل ومتكامل
- TypeScript مدمج
- حقن التبعيات
- أدوات CLI قوية

## المقارنة

### سهولة التعلم

**React:** منحنى تعلم متوسط. يتطلب فهم JSX ومفاهيم مثل الحالة والخصائص. قد يكون من الصعب على المبتدئين فهم مفهوم المكونات وتدفق البيانات في البداية.

**Vue:** منحنى تعلم منخفض. يستخدم قوالب HTML تقليدية مع توجيهات خاصة، مما يجعله أقرب إلى HTML التقليدي. الوثائق ممتازة وسهلة الفهم.

**Angular:** منحنى تعلم مرتفع. يتطلب فهم TypeScript، حقن التبعيات، والعديد من المفاهيم الأخرى. يعتبر الأكثر تعقيداً من بين الثلاثة للمبتدئين.

### الأداء

جميع الأطر الثلاثة تقدم أداءً ممتازاً في معظم السيناريوهات. ومع ذلك:

**React:** يتميز بأداء جيد جداً بفضل Virtual DOM وخوارزميات المقارنة الفعالة.

**Vue:** أداء مشابه لـ React، وفي بعض الحالات قد يكون أفضل قليلاً في التحديثات الصغيرة.

**Angular:** أداء جيد، لكنه قد يكون أبطأ قليلاً في التطبيقات الصغيرة بسبب حجمه الأكبر. ومع ذلك، يتفوق في التطبيقات الكبيرة والمعقدة.

### حجم المكتبة

**React:** صغير نسبياً (حوالي 100KB)، لكن غالباً ما يحتاج إلى مكتبات إضافية لوظائف مثل التوجيه وإدارة الحالة.

**Vue:** صغير جداً (حوالي 80KB) ويتضمن معظم الوظائف الأساسية.

**Angular:** الأكبر من بين الثلاثة (حوالي 500KB) لكنه يتضمن كل ما تحتاجه لبناء تطبيق كامل.

### المرونة والنظام البيئي

**React:** مرن للغاية مع نظام بيئي ضخم. يمكن استخدامه مع العديد من المكتبات الأخرى. Redux هو الخيار الشائع لإدارة الحالة.

**Vue:** مرونة جيدة مع نظام بيئي متنامي. يوفر Vuex لإدارة الحالة و Vue Router للتوجيه.

**Angular:** أقل مرونة لكنه يوفر حلاً شاملاً. يأتي مع كل ما تحتاجه من البداية، مما يقلل من الحاجة إلى مكتبات خارجية.

### دعم الشركات والمجتمع

**React:** مدعوم من Facebook مع مجتمع ضخم ونشط.

**Vue:** مدعوم من مجتمع المطورين، مع تمويل جماعي. مجتمع متنامي بسرعة.

**Angular:** مدعوم من Google مع مجتمع كبير ومستقر.

## متى تستخدم كل إطار؟

### استخدم React عندما:

- تحتاج إلى مرونة عالية في بناء واجهة المستخدم
- تعمل على تطبيق أحادي الصفحة (SPA) معقد
- لديك فريق على دراية بـ JavaScript الحديثة
- تحتاج إلى أداء عالٍ مع تحديثات متكررة للواجهة

### استخدم Vue عندما:

- تبدأ مشروعاً جديداً وتريد منحنى تعلم منخفض
- تحتاج إلى دمج إطار العمل مع مشروع حالي تدريجياً
- تفضل بناء جملة أقرب إلى HTML التقليدي
- تحتاج إلى إطار عمل خفيف وسريع

### استخدم Angular عندما:

- تعمل على تطبيق كبير ومعقد
- تحتاج إلى هيكل وقواعد صارمة
- تفضل استخدام TypeScript
- تحتاج إلى حل شامل من البداية

## خاتمة

لا يوجد إطار عمل "أفضل" بشكل مطلق - كل منها له نقاط قوته وضعفه. اختيار الإطار المناسب يعتمد على متطلبات مشروعك، خبرة فريقك، وتفضيلاتك الشخصية.

React يوفر مرونة عالية وأداء ممتاز، Vue يتميز بسهولة التعلم والبساطة، بينما يقدم Angular حلاً شاملاً ومتكاملاً للمشاريع الكبيرة.

في النهاية، جميع هذه الأطر قادرة على إنتاج تطبيقات ويب عالية الجودة. الأهم هو اختيار الأداة المناسبة للمهمة المناسبة والاستمرار في تطوير مهاراتك في استخدامها.""",
            "author_id": 2,
            "is_published": True,
            "category_ids": [1, 2]
        },
        {
            "title": "مقدمة في الذكاء الاصطناعي وتطبيقاته في البرمجة",
            "content": """# مقدمة في الذكاء الاصطناعي وتطبيقاته في البرمجة

## مقدمة

الذكاء الاصطناعي (AI) هو أحد أكثر المجالات إثارة وتطوراً في عالم التكنولوجيا اليوم. من المساعدين الصوتيين مثل Siri و Alexa، إلى السيارات ذاتية القيادة، وأنظمة التوصيات في منصات البث والتسوق، أصبح الذكاء الاصطناعي جزءاً لا يتجزأ من حياتنا اليومية.

في هذا المقال، سنستكشف ماهية الذكاء الاصطناعي، وكيف يمكن للمبرمجين الاستفادة من تقنياته، وبعض التطبيقات العملية له في مجال البرمجة.

## ما هو الذكاء الاصطناعي؟

الذكاء الاصطناعي هو فرع من علوم الحاسوب يهدف إلى إنشاء أنظمة قادرة على أداء مهام تتطلب عادةً ذكاءً بشرياً. هذه المهام تشمل:

- التعرف على الكلام والصور
- اتخاذ القرارات
- الترجمة بين اللغات
- فهم اللغة الطبيعية
- التعلم والتكيف

يمكن تقسيم الذكاء الاصطناعي إلى نوعين رئيسيين:

1. **الذكاء الاصطناعي الضيق (ANI)**: مصمم لأداء مهمة محددة، مثل التعرف على الوجوه أو قيادة السيارة.
2. **الذكاء الاصطناعي العام (AGI)**: قادر على فهم وتعلم وتطبيق المعرفة عبر مجموعة واسعة من المهام، مشابه للذكاء البشري.

حالياً، معظم تطبيقات الذكاء الاصطناعي تندرج تحت فئة الذكاء الاصطناعي الضيق.

## تعلم الآلة: العمود الفقري للذكاء الاصطناعي

تعلم الآلة (Machine Learning) هو مجموعة فرعية من الذكاء الاصطناعي تركز على تطوير خوارزميات تسمح للأنظمة بالتعلم من البيانات وتحسين أدائها دون برمجة صريحة.

هناك ثلاثة أنواع رئيسية من تعلم الآلة:

1. **التعلم الخاضع للإشراف (Supervised Learning)**: يتعلم النموذج من بيانات مُصنفة مسبقاً.
2. **التعلم غير الخاضع للإشراف (Unsupervised Learning)**: يكتشف النموذج الأنماط في البيانات غير المصنفة.
3. **التعلم المعزز (Reinforcement Learning)**: يتعلم النموذج من خلال التجربة والخطأ، مع مكافآت للإجراءات الصحيحة.

## التعلم العميق: الجيل التالي

التعلم العميق (Deep Learning) هو مجموعة فرعية من تعلم الآلة تستخدم الشبكات العصبية متعددة الطبقات لتحليل البيانات. هذه التقنية حققت نجاحات كبيرة في مجالات مثل:

- معالجة اللغة الطبيعية (NLP)
- رؤية الحاسوب
- توليد المحتوى (نصوص، صور، موسيقى)

## تطبيقات الذكاء الاصطناعي في البرمجة

### 1. مساعدات البرمجة الذكية

أدوات مثل GitHub Copilot و Tabnine تستخدم نماذج لغوية كبيرة لاقتراح الكود أثناء الكتابة. هذه الأدوات تحلل السياق وتقترح أكواداً مناسبة، مما يزيد من إنتاجية المبرمجين.

### 2. اختبار البرمجيات

يمكن للذكاء الاصطناعي أتمتة عملية اختبار البرمجيات من خلال:
- توليد حالات اختبار
- اكتشاف الأخطاء البرمجية
- تحسين تغطية الاختبار

### 3. تحسين الكود

أدوات مثل SonarQube تستخدم تقنيات الذكاء الاصطناعي لتحليل الكود واقتراح تحسينات للجودة والأداء والأمان.

### 4. تحليل البيانات

مكتبات مثل scikit-learn و TensorFlow و PyTorch تسهل على المبرمجين دمج قدرات تعلم الآلة في تطبيقاتهم لتحليل البيانات واستخراج الرؤى منها.

### 5. واجهات المستخدم الذكية

يمكن استخدام الذكاء الاصطناعي لإنشاء واجهات مستخدم تتكيف مع سلوك المستخدم وتفضيلاته، مما يحسن تجربة المستخدم.

### 6. معالجة اللغة الطبيعية

مكتبات مثل spaCy و NLTK تمكن المبرمجين من دمج قدرات معالجة اللغة الطبيعية في تطبيقاتهم، مثل:
- تحليل المشاعر
- استخراج الكيانات
- تلخيص النصوص
- الترجمة الآلية

## كيفية البدء في الذكاء الاصطناعي كمبرمج

### 1. تعلم الأساسيات

- لغة Python (الأكثر استخداماً في مجال الذكاء الاصطناعي)
- أساسيات الإحصاء والاحتمالات
- الجبر الخطي
- التفاضل والتكامل

### 2. استكشف المكتبات والأدوات

- **scikit-learn**: مكتبة بسيطة وفعالة لتعلم الآلة
- **TensorFlow/PyTorch**: أطر عمل للتعلم العميق
- **Pandas**: لمعالجة وتحليل البيانات
- **NumPy**: للعمليات الرياضية المتقدمة
- **Matplotlib/Seaborn**: لتصور البيانات

### 3. العمل على مشاريع عملية

- تحليل مجموعات البيانات العامة
- المشاركة في تحديات Kaggle
- بناء تطبيقات بسيطة تستخدم الذكاء الاصطناعي

### 4. متابعة آخر التطورات

- الاشتراك في النشرات الإخبارية المتخصصة
- متابعة الأبحاث الجديدة على arXiv
- المشاركة في المؤتمرات والندوات عبر الإنترنت

## التحديات والاعتبارات الأخلاقية

مع تزايد استخدام الذكاء الاصطناعي، تظهر تحديات وقضايا أخلاقية يجب على المبرمجين مراعاتها:

- **الخصوصية**: كيفية جمع واستخدام بيانات المستخدمين
- **التحيز**: ضمان عدم تعزيز النماذج للتحيزات الموجودة في البيانات
- **الشفافية**: القدرة على شرح كيفية اتخاذ النماذج للقرارات
- **المساءلة**: تحديد المسؤولية عن قرارات الذكاء الاصطناعي
- **الأمان**: حماية الأنظمة من الاستغلال والهجمات

## خاتمة

الذكاء الاصطناعي يغير طريقة كتابتنا للبرمجيات وتفاعلنا معها. كمبرمجين، فهم أساسيات الذكاء الاصطناعي وتطبيقاته يمكن أن يفتح آفاقاً جديدة ويعزز قدراتنا على حل المشكلات المعقدة.

سواء كنت تستخدم أدوات الذكاء الاصطناعي لتحسين إنتاجيتك، أو تبني تطبيقات ذكية، أو تعمل على تطوير خوارزميات جديدة، فإن هذا المجال يقدم فرصاً هائلة للابتكار والنمو.

المستقبل ينتمي للمبرمجين الذين يمكنهم الجمع بين مهارات البرمجة التقليدية وفهم تقنيات الذكاء الاصطناعي لإنشاء الجيل التالي من التطبيقات الذكية.""",
            "author_id": 4,
            "is_published": True,
            "category_ids": [1, 5]
        }
    ]
    
    for article_data in articles:
        # Extract category IDs
        category_ids = article_data.pop('category_ids', [])
        
        # Create article
        article = Article(**article_data)
        db.session.add(article)
        db.session.flush()  # Get article ID
        
        # Add categories
        for category_id in category_ids:
            article_category = ArticleCategory(article_id=article.id, category_id=category_id)
            db.session.add(article_category)
    
    db.session.commit()
    print(f"Added {len(articles)} articles")

def seed_games():
    """Seed games data"""
    print("Seeding games...")
    
    games = [
        {
            "title": "Code Breaker",
            "description": "لعبة تحدي برمجية تختبر مهاراتك في حل المشكلات البرمجية. عليك فك شفرة الكود وإصلاح الأخطاء في وقت محدد.",
            "game_url": "https://example.com/games/code-breaker",
            "thumbnail_url": "https://example.com/images/code-breaker.jpg",
            "programming_language": "JavaScript",
            "difficulty_level": "متوسط",
            "instructions": "استخدم لوحة المفاتيح للتنقل بين أجزاء الكود. اضغط Enter لتأكيد الإجابة."
        },
        {
            "title": "Python Quest",
            "description": "مغامرة تعليمية تأخذك في رحلة لتعلم Python من خلال حل الألغاز وإكمال التحديات البرمجية.",
            "game_url": "https://example.com/games/python-quest",
            "thumbnail_url": "https://example.com/images/python-quest.jpg",
            "programming_language": "Python",
            "difficulty_level": "مبتدئ",
            "instructions": "اكتب الكود في محرر النصوص واضغط على زر التشغيل للتحقق من الإجابة."
        },
        {
            "title": "CSS Battle",
            "description": "تحدي تصميم يختبر مهاراتك في CSS. عليك إعادة إنشاء التصميم المعروض باستخدام أقل عدد ممكن من أكواد CSS.",
            "game_url": "https://example.com/games/css-battle",
            "thumbnail_url": "https://example.com/images/css-battle.jpg",
            "programming_language": "CSS",
            "difficulty_level": "متقدم",
            "instructions": "اكتب كود CSS في المحرر لمطابقة الصورة المعروضة. يتم احتساب النقاط بناءً على دقة المطابقة وحجم الكود."
        },
        {
            "title": "Algorithm Adventure",
            "description": "لعبة مغامرة تعليمية تركز على الخوارزميات وهياكل البيانات. تعلم وطبق مفاهيم مثل البحث والفرز وحل المشكلات.",
            "game_url": "https://example.com/games/algorithm-adventure",
            "thumbnail_url": "https://example.com/images/algorithm-adventure.jpg",
            "programming_language": "متعدد",
            "difficulty_level": "متوسط",
            "instructions": "اختر الخوارزمية المناسبة لكل تحدي واكتب الكود لتنفيذها."
        },
        {
            "title": "SQL Island",
            "description": "مغامرة تفاعلية لتعلم SQL. أنت عالق على جزيرة وعليك استخدام استعلامات SQL للتفاعل مع سكان الجزيرة والهروب.",
            "game_url": "https://example.com/games/sql-island",
            "thumbnail_url": "https://example.com/images/sql-island.jpg",
            "programming_language": "SQL",
            "difficulty_level": "مبتدئ",
            "instructions": "اكتب استعلامات SQL للتفاعل مع عناصر اللعبة والتقدم في القصة."
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
            "tool_type": "code_completion",
            "usage_instructions": "اكتب بداية الكود وسيقوم المساعد باقتراح الإكمال المناسب.",
            "example_prompts": json.dumps([
                "دالة لحساب مجموع عناصر مصفوفة",
                "كود HTML لإنشاء نموذج تسجيل",
                "دالة للتحقق من صحة البريد الإلكتروني"
            ])
        },
        {
            "name": "Bug Hunter",
            "description": "أداة تحليل أكواد تكتشف الأخطاء البرمجية وتقترح إصلاحات لها.",
            "api_endpoint": "/api/ai-tools/bug-hunter",
            "tool_type": "code_analysis",
            "usage_instructions": "قم بنسخ الكود الذي تريد فحصه وانقر على زر 'تحليل'.",
            "example_prompts": json.dumps([
                "تحليل كود JavaScript للبحث عن أخطاء",
                "فحص كود Python للتأكد من جودته",
                "اكتشاف مشاكل الأداء في كود SQL"
            ])
        },
        {
            "name": "Code Translator",
            "description": "أداة لترجمة الكود بين لغات البرمجة المختلفة مع الحفاظ على الوظائف.",
            "api_endpoint": "/api/ai-tools/code-translator",
            "tool_type": "code_translation",
            "usage_instructions": "اختر لغة المصدر ولغة الهدف، ثم أدخل الكود المراد ترجمته.",
            "example_prompts": json.dumps([
                "ترجمة كود من Python إلى JavaScript",
                "تحويل دالة من Java إلى C#",
                "ترجمة استعلام SQL إلى Mongoose"
            ])
        },
        {
            "name": "Code Explainer",
            "description": "أداة تشرح الكود بلغة بسيطة وتوضح كيفية عمله خطوة بخطوة.",
            "api_endpoint": "/api/ai-tools/code-explainer",
            "tool_type": "code_explanation",
            "usage_instructions": "أدخل الكود الذي تريد شرحه واختر مستوى التفصيل المطلوب.",
            "example_prompts": json.dumps([
                "شرح خوارزمية البحث الثنائي",
                "توضيح كيفية عمل دالة async/await",
                "شرح كود React لمكون تفاعلي"
            ])
        },
        {
            "name": "Code Optimizer",
            "description": "أداة تحسين الكود لزيادة الأداء وتقليل استهلاك الموارد.",
            "api_endpoint": "/api/ai-tools/code-optimizer",
            "tool_type": "code_optimization",
            "usage_instructions": "أدخل الكود المراد تحسينه واختر نوع التحسين (سرعة، ذاكرة، قابلية القراءة).",
            "example_prompts": json.dumps([
                "تحسين أداء حلقة تكرارية",
                "تقليل استهلاك الذاكرة في كود معالجة البيانات",
                "تحسين قابلية قراءة كود معقد"
            ])
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

def seed_ratings_and_progress():
    """Seed ratings and progress data"""
    print("Seeding ratings and progress data...")
    
    # Course ratings
    for i in range(1, 14):  # For each course
        num_ratings = random.randint(5, 20)
        for j in range(num_ratings):
            user_id = random.randint(1, 5)  # Random user
            rating = random.randint(3, 5)  # Ratings between 3-5
            
            course_rating = CourseRating(
                user_id=user_id,
                course_id=i,
                rating=rating,
                review=f"تقييم للدورة {i} من المستخدم {user_id}. {'دورة ممتازة ومفيدة جداً!' if rating >= 4 else 'دورة جيدة ولكن تحتاج إلى بعض التحسينات.'}"
            )
            db.session.add(course_rating)
    
    # Quiz attempts
    for i in range(1, 4):  # For each quiz
        num_attempts = random.randint(5, 15)
        for j in range(num_attempts):
            user_id = random.randint(1, 5)  # Random user
            score = random.randint(5, 10)  # Score between 5-10
            
            quiz_attempt = UserQuizAttempt(
                user_id=user_id,
                quiz_id=i,
                score=score,
                answers_submitted=json.dumps([
                    {"question_id": 1, "answer": "25" if i == 1 else "object"},
                    {"question_id": 2, "answer": "float" if i == 1 else "[6, 8, 10]"}
                ])
            )
            db.session.add(quiz_attempt)
    
    # Game scores
    for i in range(1, 6):  # For each game
        num_scores = random.randint(3, 10)
        for j in range(num_scores):
            user_id = random.randint(1, 5)  # Random user
            score = random.randint(50, 100)  # Score between 50-100
            
            game_score = UserGameScore(
                user_id=user_id,
                game_id=i,
                score=score,
                completion_time_seconds=random.randint(300, 900)  # 5-15 minutes
            )
            db.session.add(game_score)
    
    # Course progress
    for user_id in range(1, 6):  # For each user
        num_courses = random.randint(2, 5)
        for i in range(num_courses):
            course_id = random.randint(1, 13)
            progress_percentage = random.randint(10, 100)
            
            course_progress = UserCourseProgress(
                user_id=user_id,
                course_id=course_id,
                progress_percentage=progress_percentage,
                last_accessed_lesson_id=random.randint(1, 20)
            )
            db.session.add(course_progress)
    
    db.session.commit()
    print("Added ratings, quiz attempts, game scores, and course progress data")

def main():
    """Main function to seed all data"""
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Seed data
        seed_categories()
        seed_users()
        seed_courses()
        seed_quizzes()
        seed_articles()
        seed_games()
        seed_ai_tools()
        seed_forums()
        seed_ratings_and_progress()
        
        print("Data seeding completed successfully!")

if __name__ == "__main__":
    main()

