# دليل المطور لموقع Code Aura

## مقدمة

هذا الدليل مخصص للمطورين الذين يرغبون في فهم بنية وتنظيم كود موقع Code Aura، سواء للصيانة أو التطوير أو إضافة ميزات جديدة. يوفر هذا الدليل نظرة عامة على الهيكل التقني للموقع، بما في ذلك الواجهة الأمامية والخلفية وقاعدة البيانات، بالإضافة إلى إرشادات التطوير والنشر.

## جدول المحتويات

1. [نظرة عامة على الهيكل التقني](#نظرة-عامة-على-الهيكل-التقني)
2. [إعداد بيئة التطوير](#إعداد-بيئة-التطوير)
3. [الباك إند (Flask)](#الباك-إند-flask)
4. [الفرونت إند (React)](#الفرونت-إند-react)
5. [قاعدة البيانات](#قاعدة-البيانات)
6. [واجهات برمجة التطبيقات (APIs)](#واجهات-برمجة-التطبيقات-apis)
7. [المصادقة والتفويض](#المصادقة-والتفويض)
8. [تكامل الذكاء الاصطناعي](#تكامل-الذكاء-الاصطناعي)
9. [اختبار الكود](#اختبار-الكود)
10. [النشر والتحديث](#النشر-والتحديث)
11. [أفضل الممارسات](#أفضل-الممارسات)
12. [استكشاف الأخطاء وإصلاحها](#استكشاف-الأخطاء-وإصلاحها)
13. [الموارد والمراجع](#الموارد-والمراجع)

## نظرة عامة على الهيكل التقني

موقع Code Aura مبني باستخدام هيكل تطبيق ويب حديث يتكون من:

### الواجهة الأمامية (Frontend)

- **إطار العمل**: React.js
- **لغات البرمجة**: JavaScript/TypeScript، HTML، CSS
- **مكتبات رئيسية**: React Router، Axios، Monaco Editor
- **أدوات البناء**: Vite

### الباك إند (Backend)

- **إطار العمل**: Flask (Python)
- **لغة البرمجة**: Python 3.11
- **مكتبات رئيسية**: SQLAlchemy، Flask-RESTful، Flask-JWT-Extended، Authlib

### قاعدة البيانات

- **نظام إدارة قواعد البيانات**: PostgreSQL
- **أداة ORM**: SQLAlchemy

### خدمات الطرف الثالث

- **المصادقة**: OAuth (Google، Facebook، GitHub)
- **الذكاء الاصطناعي**: OpenAI API
- **تخزين الملفات**: AWS S3 (اختياري)

### هيكل المشروع

```
code_aura/
├── backend/                  # مشروع الباك إند (Flask)
│   ├── src/
│   │   ├── config/           # ملفات الإعدادات
│   │   ├── models/           # نماذج قاعدة البيانات
│   │   ├── routes/           # مسارات API
│   │   ├── scripts/          # سكريبتات مساعدة
│   │   ├── services/         # خدمات تطبيقية
│   │   ├── static/           # ملفات ثابتة
│   │   ├── templates/        # قوالب HTML
│   │   ├── utils/            # أدوات مساعدة
│   │   └── main.py           # نقطة الدخول الرئيسية
│   ├── tests/                # اختبارات الباك إند
│   ├── .env                  # متغيرات البيئة
│   └── requirements.txt      # تبعيات Python
│
├── frontend/                 # مشروع الفرونت إند (React)
│   ├── public/               # ملفات عامة
│   ├── src/
│   │   ├── assets/           # الصور والأصول
│   │   ├── components/       # مكونات React
│   │   ├── contexts/         # سياقات React
│   │   ├── hooks/            # خطافات React المخصصة
│   │   ├── pages/            # صفحات التطبيق
│   │   ├── services/         # خدمات API
│   │   ├── styles/           # ملفات CSS
│   │   ├── utils/            # أدوات مساعدة
│   │   ├── App.jsx           # مكون التطبيق الرئيسي
│   │   └── main.jsx          # نقطة الدخول الرئيسية
│   ├── tests/                # اختبارات الفرونت إند
│   └── package.json          # تبعيات Node.js
│
└── docs/                     # وثائق المشروع
```

## إعداد بيئة التطوير

### المتطلبات الأساسية

- Node.js (v16+)
- Python (v3.11+)
- PostgreSQL (v14+)
- Git

### خطوات إعداد بيئة التطوير

#### 1. استنساخ المستودع

```bash
git clone https://github.com/your-organization/code-aura.git
cd code-aura
```

#### 2. إعداد الباك إند

```bash
cd backend

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# على Windows
venv\Scripts\activate
# على macOS/Linux
source venv/bin/activate

# تثبيت التبعيات
pip install -r requirements.txt

# إنشاء ملف .env
cp .env.example .env
# قم بتعديل ملف .env بإعداداتك المحلية

# إنشاء قاعدة البيانات
flask db upgrade

# تشغيل سكريبت تعبئة البيانات الأولية
python src/scripts/seed_data.py

# تشغيل الخادم
flask run
```

#### 3. إعداد الفرونت إند

```bash
cd frontend

# تثبيت التبعيات
npm install

# إنشاء ملف .env
cp .env.example .env
# قم بتعديل ملف .env بإعداداتك المحلية

# تشغيل خادم التطوير
npm run dev
```

#### 4. الوصول إلى التطبيق

- الباك إند: http://localhost:5000
- الفرونت إند: http://localhost:3000

## الباك إند (Flask)

### هيكل المشروع

```
backend/
├── src/
│   ├── config/               # ملفات الإعدادات
│   │   ├── __init__.py
│   │   ├── config.py         # إعدادات التطبيق
│   │   └── oauth.py          # إعدادات OAuth
│   │
│   ├── models/               # نماذج قاعدة البيانات
│   │   ├── __init__.py
│   │   ├── database.py       # إعداد قاعدة البيانات
│   │   ├── user.py           # نموذج المستخدم
│   │   ├── course.py         # نموذج الدورة
│   │   ├── quiz.py           # نموذج الاختبار
│   │   ├── game.py           # نموذج اللعبة
│   │   ├── ai_tool.py        # نموذج أداة الذكاء الاصطناعي
│   │   ├── article.py        # نموذج المقال
│   │   └── forum.py          # نموذج المنتدى
│   │
│   ├── routes/               # مسارات API
│   │   ├── __init__.py
│   │   ├── auth.py           # مسارات المصادقة
│   │   ├── user.py           # مسارات المستخدم
│   │   ├── course.py         # مسارات الدورة
│   │   ├── quiz.py           # مسارات الاختبار
│   │   ├── game.py           # مسارات اللعبة
│   │   ├── ai_tool.py        # مسارات أداة الذكاء الاصطناعي
│   │   ├── article.py        # مسارات المقال
│   │   ├── forum.py          # مسارات المنتدى
│   │   └── admin.py          # مسارات الأدمن
│   │
│   ├── scripts/              # سكريبتات مساعدة
│   │   ├── create_admin.py   # إنشاء مستخدم أدمن
│   │   └── seed_data.py      # تعبئة البيانات الأولية
│   │
│   ├── services/             # خدمات تطبيقية
│   │   ├── __init__.py
│   │   ├── auth_service.py   # خدمة المصادقة
│   │   ├── user_service.py   # خدمة المستخدم
│   │   └── ai_service.py     # خدمة الذكاء الاصطناعي
│   │
│   ├── utils/                # أدوات مساعدة
│   │   ├── __init__.py
│   │   ├── decorators.py     # مزخرفات مخصصة
│   │   ├── validators.py     # أدوات التحقق
│   │   └── helpers.py        # دوال مساعدة
│   │
│   └── main.py               # نقطة الدخول الرئيسية
```

### نقطة الدخول الرئيسية (main.py)

ملف `main.py` هو نقطة الدخول الرئيسية للتطبيق. يقوم بإنشاء تطبيق Flask وتكوينه وتسجيل جميع مسارات API.

```python
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from src.config.config import Config
from src.models.database import db
from src.routes import register_routes

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # تهيئة الإضافات
    db.init_app(app)
    Migrate(app, db)
    CORS(app)
    
    # تسجيل المسارات
    register_routes(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### نماذج قاعدة البيانات

نماذج قاعدة البيانات تمثل الكيانات الرئيسية في التطبيق. فيما يلي مثال على نموذج المستخدم:

```python
# src/models/user.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    profile = db.relationship('UserProfile', backref='user', uselist=False)
    courses = db.relationship('CourseEnrollment', backref='user')
    quiz_attempts = db.relationship('QuizAttempt', backref='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

### مسارات API

مسارات API تعالج طلبات HTTP وتستجيب لها. فيما يلي مثال على مسارات المصادقة:

```python
# src/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from src.models.user import User
from src.models.database import db
from src.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # التحقق من البيانات
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({'message': 'البيانات غير كاملة'}), 400
    
    # التحقق من وجود المستخدم
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'البريد الإلكتروني مستخدم بالفعل'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'اسم المستخدم مستخدم بالفعل'}), 400
    
    # إنشاء المستخدم
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'تم إنشاء المستخدم بنجاح'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # التحقق من البيانات
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'البيانات غير كاملة'}), 400
    
    # التحقق من المستخدم
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'بيانات الدخول غير صحيحة'}), 401
    
    # إنشاء توكن
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'المستخدم غير موجود'}), 404
    
    return jsonify(user.to_dict()), 200
```

### خدمات

الخدمات تحتوي على منطق الأعمال الرئيسي للتطبيق. فيما يلي مثال على خدمة الذكاء الاصطناعي:

```python
# src/services/ai_service.py
import os
import openai
from src.config.config import Config

class AIService:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
    
    def generate_code(self, prompt, language):
        """
        توليد كود من وصف نصي
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"أنت مساعد برمجة محترف. قم بتوليد كود {language} بناءً على الوصف التالي."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"خطأ في توليد الكود: {str(e)}")
            return None
    
    def explain_code(self, code):
        """
        شرح الكود بلغة بسيطة
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت مساعد برمجة محترف. قم بشرح الكود التالي بلغة بسيطة ومفهومة."},
                    {"role": "user", "content": code}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"خطأ في شرح الكود: {str(e)}")
            return None
    
    def fix_code(self, code, language):
        """
        تصحيح الأخطاء في الكود
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"أنت مساعد برمجة محترف. قم بتصحيح الأخطاء في كود {language} التالي."},
                    {"role": "user", "content": code}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"خطأ في تصحيح الكود: {str(e)}")
            return None
    
    def translate_code(self, code, source_language, target_language):
        """
        تحويل الكود من لغة برمجة إلى أخرى
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"أنت مساعد برمجة محترف. قم بتحويل الكود من {source_language} إلى {target_language}."},
                    {"role": "user", "content": code}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"خطأ في تحويل الكود: {str(e)}")
            return None
```

## الفرونت إند (React)

### هيكل المشروع

```
frontend/
├── public/                   # ملفات عامة
│   ├── favicon.ico
│   └── index.html
│
├── src/
│   ├── assets/               # الصور والأصول
│   │   ├── images/
│   │   └── logo.svg
│   │
│   ├── components/           # مكونات React
│   │   ├── auth/             # مكونات المصادقة
│   │   ├── courses/          # مكونات الدورات
│   │   ├── quizzes/          # مكونات الاختبارات
│   │   ├── code-editor/      # مكونات محرر الأكواد
│   │   ├── ai-tools/         # مكونات أدوات الذكاء الاصطناعي
│   │   ├── games/            # مكونات الألعاب
│   │   ├── forums/           # مكونات المنتديات
│   │   ├── articles/         # مكونات المقالات
│   │   ├── admin/            # مكونات لوحة الأدمن
│   │   ├── layout/           # مكونات التخطيط
│   │   └── common/           # مكونات مشتركة
│   │
│   ├── contexts/             # سياقات React
│   │   ├── AuthContext.jsx   # سياق المصادقة
│   │   └── ThemeContext.jsx  # سياق السمة
│   │
│   ├── hooks/                # خطافات React المخصصة
│   │   ├── useAuth.js        # خطاف المصادقة
│   │   └── useTheme.js       # خطاف السمة
│   │
│   ├── pages/                # صفحات التطبيق
│   │   ├── HomePage.jsx      # الصفحة الرئيسية
│   │   ├── CoursesPage.jsx   # صفحة الدورات
│   │   ├── QuizzesPage.jsx   # صفحة الاختبارات
│   │   ├── CodeEditorPage.jsx # صفحة محرر الأكواد
│   │   ├── AIToolsPage.jsx   # صفحة أدوات الذكاء الاصطناعي
│   │   ├── GamesPage.jsx     # صفحة الألعاب
│   │   ├── ForumsPage.jsx    # صفحة المنتديات
│   │   ├── ArticlesPage.jsx  # صفحة المقالات
│   │   ├── ProfilePage.jsx   # صفحة الملف الشخصي
│   │   ├── SettingsPage.jsx  # صفحة الإعدادات
│   │   └── admin/            # صفحات لوحة الأدمن
│   │
│   ├── services/             # خدمات API
│   │   ├── api.js            # إعداد Axios
│   │   ├── authService.js    # خدمة المصادقة
│   │   ├── courseService.js  # خدمة الدورات
│   │   ├── quizService.js    # خدمة الاختبارات
│   │   ├── aiService.js      # خدمة الذكاء الاصطناعي
│   │   └── adminService.js   # خدمة الأدمن
│   │
│   ├── styles/               # ملفات CSS
│   │   ├── global.css        # أنماط عامة
│   │   └── variables.css     # متغيرات CSS
│   │
│   ├── utils/                # أدوات مساعدة
│   │   ├── formatters.js     # دوال تنسيق
│   │   ├── validators.js     # دوال التحقق
│   │   └── helpers.js        # دوال مساعدة
│   │
│   ├── App.jsx               # مكون التطبيق الرئيسي
│   └── main.jsx              # نقطة الدخول الرئيسية
│
├── .env                      # متغيرات البيئة
└── package.json              # تبعيات Node.js
```

### نقطة الدخول الرئيسية (main.jsx)

ملف `main.jsx` هو نقطة الدخول الرئيسية للتطبيق. يقوم بتحميل مكون التطبيق الرئيسي وتثبيته في DOM.

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import './styles/global.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <ThemeProvider>
          <App />
        </ThemeProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
```

### مكون التطبيق الرئيسي (App.jsx)

ملف `App.jsx` هو المكون الرئيسي للتطبيق. يحتوي على تكوين المسارات وهيكل التطبيق العام.

```jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import { useTheme } from './hooks/useTheme';

// مكونات التخطيط
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// مكونات المسارات
import PrivateRoute from './components/auth/PrivateRoute';
import AdminRoute from './components/auth/AdminRoute';

// الصفحات
import HomePage from './pages/HomePage';
import CoursesPage from './pages/CoursesPage';
import CourseDetailPage from './pages/CourseDetailPage';
import QuizzesPage from './pages/QuizzesPage';
import QuizDetailPage from './pages/QuizDetailPage';
import CodeEditorPage from './pages/CodeEditorPage';
import AIToolsPage from './pages/AIToolsPage';
import GamesPage from './pages/GamesPage';
import ForumsPage from './pages/ForumsPage';
import ArticlesPage from './pages/ArticlesPage';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import NotFoundPage from './pages/NotFoundPage';

// صفحات الأدمن
import AdminDashboardPage from './pages/admin/AdminDashboardPage';
import AdminUsersPage from './pages/admin/AdminUsersPage';
import AdminCoursesPage from './pages/admin/AdminCoursesPage';

import './App.css';

function App() {
  const { isAuthenticated, loading } = useAuth();
  const { theme } = useTheme();

  if (loading) {
    return <div className="loading">جاري التحميل...</div>;
  }

  return (
    <div className={`app ${theme}`}>
      <Navbar />
      <main className="main-content">
        <Routes>
          {/* المسارات العامة */}
          <Route path="/" element={<HomePage />} />
          <Route path="/courses" element={<CoursesPage />} />
          <Route path="/courses/:id" element={<CourseDetailPage />} />
          <Route path="/quizzes" element={<QuizzesPage />} />
          <Route path="/quizzes/:id" element={<QuizDetailPage />} />
          <Route path="/articles" element={<ArticlesPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* المسارات الخاصة */}
          <Route path="/code-editor" element={
            <PrivateRoute>
              <CodeEditorPage />
            </PrivateRoute>
          } />
          <Route path="/ai-tools" element={
            <PrivateRoute>
              <AIToolsPage />
            </PrivateRoute>
          } />
          <Route path="/games" element={
            <PrivateRoute>
              <GamesPage />
            </PrivateRoute>
          } />
          <Route path="/forums" element={
            <PrivateRoute>
              <ForumsPage />
            </PrivateRoute>
          } />
          <Route path="/profile" element={
            <PrivateRoute>
              <ProfilePage />
            </PrivateRoute>
          } />
          <Route path="/settings" element={
            <PrivateRoute>
              <SettingsPage />
            </PrivateRoute>
          } />

          {/* مسارات الأدمن */}
          <Route path="/admin" element={
            <AdminRoute>
              <AdminDashboardPage />
            </AdminRoute>
          } />
          <Route path="/admin/users" element={
            <AdminRoute>
              <AdminUsersPage />
            </AdminRoute>
          } />
          <Route path="/admin/courses" element={
            <AdminRoute>
              <AdminCoursesPage />
            </AdminRoute>
          } />

          {/* مسار غير موجود */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
```

### سياق المصادقة (AuthContext.jsx)

سياق المصادقة يوفر حالة المصادقة والوظائف ذات الصلة لجميع مكونات التطبيق.

```jsx
import React, { createContext, useState, useEffect } from 'react';
import authService from '../services/authService';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // التحقق من حالة المصادقة عند تحميل التطبيق
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const userData = await authService.getProfile();
          setUser(userData);
        }
      } catch (err) {
        console.error('خطأ في التحقق من المصادقة:', err);
        localStorage.removeItem('token');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      setError(null);
      const data = await authService.login(email, password);
      localStorage.setItem('token', data.token);
      setUser(data.user);
      return data.user;
    } catch (err) {
      setError(err.response?.data?.message || 'حدث خطأ أثناء تسجيل الدخول');
      throw err;
    }
  };

  const register = async (username, email, password) => {
    try {
      setError(null);
      const data = await authService.register(username, email, password);
      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'حدث خطأ أثناء التسجيل');
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
```

### خدمات API

خدمات API تتعامل مع طلبات HTTP إلى الباك إند. فيما يلي مثال على خدمة المصادقة:

```jsx
// src/services/authService.js
import api from './api';

const authService = {
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },

  register: async (username, email, password) => {
    const response = await api.post('/auth/register', { username, email, password });
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/auth/profile');
    return response.data;
  },

  loginWithGoogle: async (token) => {
    const response = await api.post('/auth/google', { token });
    return response.data;
  },

  loginWithFacebook: async (token) => {
    const response = await api.post('/auth/facebook', { token });
    return response.data;
  },

  loginWithGithub: async (code) => {
    const response = await api.post('/auth/github', { code });
    return response.data;
  },
};

export default authService;
```

### إعداد Axios

ملف `api.js` يقوم بإعداد مثيل Axios مع التكوين المناسب:

```jsx
// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// إضافة معترض الطلبات لإرفاق توكن المصادقة
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// إضافة معترض الاستجابات للتعامل مع الأخطاء
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // التعامل مع خطأ انتهاء صلاحية التوكن
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

## قاعدة البيانات

### مخطط قاعدة البيانات

فيما يلي مخطط قاعدة البيانات الرئيسي لموقع Code Aura:

#### جدول المستخدمين (users)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| username | VARCHAR(64) | اسم المستخدم (فريد) |
| email | VARCHAR(120) | البريد الإلكتروني (فريد) |
| password_hash | VARCHAR(128) | تجزئة كلمة المرور |
| is_admin | BOOLEAN | هل المستخدم أدمن؟ |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول ملفات المستخدمين (user_profiles)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| user_id | INTEGER | مفتاح خارجي للمستخدم |
| full_name | VARCHAR(100) | الاسم الكامل |
| bio | TEXT | نبذة شخصية |
| avatar_url | VARCHAR(255) | رابط الصورة الشخصية |
| website | VARCHAR(255) | الموقع الإلكتروني |
| github | VARCHAR(255) | حساب GitHub |
| twitter | VARCHAR(255) | حساب Twitter |
| linkedin | VARCHAR(255) | حساب LinkedIn |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول حسابات OAuth (oauth_accounts)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| user_id | INTEGER | مفتاح خارجي للمستخدم |
| provider | VARCHAR(20) | مزود المصادقة (google, facebook, github) |
| provider_user_id | VARCHAR(255) | معرف المستخدم لدى المزود |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول الدورات (courses)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| title | VARCHAR(255) | عنوان الدورة |
| description | TEXT | وصف الدورة |
| language | VARCHAR(20) | لغة الدورة (arabic, english) |
| level | VARCHAR(20) | مستوى الدورة (beginner, intermediate, advanced) |
| category_id | INTEGER | مفتاح خارجي للتصنيف |
| thumbnail_url | VARCHAR(255) | رابط الصورة المصغرة |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول دروس الدورات (course_lessons)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| course_id | INTEGER | مفتاح خارجي للدورة |
| title | VARCHAR(255) | عنوان الدرس |
| description | TEXT | وصف الدرس |
| video_url | VARCHAR(255) | رابط الفيديو |
| order | INTEGER | ترتيب الدرس في الدورة |
| duration | INTEGER | مدة الدرس بالدقائق |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول تسجيل الدورات (course_enrollments)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| user_id | INTEGER | مفتاح خارجي للمستخدم |
| course_id | INTEGER | مفتاح خارجي للدورة |
| progress | INTEGER | نسبة التقدم (0-100) |
| completed | BOOLEAN | هل تم إكمال الدورة؟ |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول تقييمات الدورات (course_ratings)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| user_id | INTEGER | مفتاح خارجي للمستخدم |
| course_id | INTEGER | مفتاح خارجي للدورة |
| rating | INTEGER | التقييم (1-5) |
| comment | TEXT | التعليق |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول الاختبارات (quizzes)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| title | VARCHAR(255) | عنوان الاختبار |
| description | TEXT | وصف الاختبار |
| programming_language | VARCHAR(50) | لغة البرمجة |
| level | VARCHAR(20) | مستوى الصعوبة (easy, medium, hard) |
| time_limit | INTEGER | الحد الزمني بالدقائق |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول أسئلة الاختبارات (quiz_questions)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| quiz_id | INTEGER | مفتاح خارجي للاختبار |
| question | TEXT | نص السؤال |
| type | VARCHAR(20) | نوع السؤال (multiple_choice, coding) |
| code_snippet | TEXT | مقتطف الكود (إن وجد) |
| points | INTEGER | النقاط |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول خيارات الأسئلة (question_options)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| question_id | INTEGER | مفتاح خارجي للسؤال |
| option_text | TEXT | نص الخيار |
| is_correct | BOOLEAN | هل الخيار صحيح؟ |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول محاولات الاختبارات (quiz_attempts)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| user_id | INTEGER | مفتاح خارجي للمستخدم |
| quiz_id | INTEGER | مفتاح خارجي للاختبار |
| score | INTEGER | النتيجة |
| time_taken | INTEGER | الوقت المستغرق بالثواني |
| completed | BOOLEAN | هل تم إكمال الاختبار؟ |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول الألعاب (games)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| title | VARCHAR(255) | عنوان اللعبة |
| description | TEXT | وصف اللعبة |
| thumbnail_url | VARCHAR(255) | رابط الصورة المصغرة |
| game_url | VARCHAR(255) | رابط اللعبة |
| category | VARCHAR(50) | فئة اللعبة |
| level | VARCHAR(20) | مستوى الصعوبة |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول أدوات الذكاء الاصطناعي (ai_tools)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| name | VARCHAR(255) | اسم الأداة |
| description | TEXT | وصف الأداة |
| icon | VARCHAR(255) | أيقونة الأداة |
| tool_type | VARCHAR(50) | نوع الأداة |
| api_endpoint | VARCHAR(255) | نقطة نهاية API |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول المقالات (articles)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| title | VARCHAR(255) | عنوان المقال |
| content | TEXT | محتوى المقال |
| author_id | INTEGER | مفتاح خارجي للمؤلف |
| category_id | INTEGER | مفتاح خارجي للتصنيف |
| thumbnail_url | VARCHAR(255) | رابط الصورة المصغرة |
| published | BOOLEAN | هل تم نشر المقال؟ |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول المنتديات (forums)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| name | VARCHAR(255) | اسم المنتدى |
| description | TEXT | وصف المنتدى |
| category | VARCHAR(50) | فئة المنتدى |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول مواضيع المنتديات (forum_topics)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| forum_id | INTEGER | مفتاح خارجي للمنتدى |
| user_id | INTEGER | مفتاح خارجي للمستخدم |
| title | VARCHAR(255) | عنوان الموضوع |
| content | TEXT | محتوى الموضوع |
| views | INTEGER | عدد المشاهدات |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول ردود المنتديات (forum_replies)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| topic_id | INTEGER | مفتاح خارجي للموضوع |
| user_id | INTEGER | مفتاح خارجي للمستخدم |
| content | TEXT | محتوى الرد |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

#### جدول التصنيفات (categories)

| العمود | النوع | الوصف |
|--------|------|--------|
| id | INTEGER | المفتاح الأساسي |
| name | VARCHAR(100) | اسم التصنيف |
| description | TEXT | وصف التصنيف |
| parent_id | INTEGER | مفتاح خارجي للتصنيف الأب |
| created_at | TIMESTAMP | تاريخ الإنشاء |
| updated_at | TIMESTAMP | تاريخ التحديث |

### إعداد قاعدة البيانات

يتم إعداد قاعدة البيانات باستخدام SQLAlchemy في ملف `database.py`:

```python
# src/models/database.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# إنشاء اصطلاحات تسمية متسقة للقيود
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
```

### ترحيلات قاعدة البيانات

يتم إدارة ترحيلات قاعدة البيانات باستخدام Flask-Migrate. فيما يلي الأوامر الأساسية:

```bash
# تهيئة ترحيلات قاعدة البيانات
flask db init

# إنشاء ترحيل جديد
flask db migrate -m "وصف التغييرات"

# تطبيق الترحيلات
flask db upgrade

# التراجع عن الترحيلات
flask db downgrade
```

## واجهات برمجة التطبيقات (APIs)

### نقاط نهاية API الرئيسية

#### المصادقة

| الطريقة | المسار | الوصف |
|--------|------|--------|
| POST | /api/auth/register | تسجيل مستخدم جديد |
| POST | /api/auth/login | تسجيل الدخول |
| GET | /api/auth/profile | الحصول على الملف الشخصي للمستخدم الحالي |
| POST | /api/auth/google | تسجيل الدخول باستخدام Google |
| POST | /api/auth/facebook | تسجيل الدخول باستخدام Facebook |
| POST | /api/auth/github | تسجيل الدخول باستخدام GitHub |

#### المستخدمين

| الطريقة | المسار | الوصف |
|--------|------|--------|
| GET | /api/users | الحصول على قائمة المستخدمين |
| GET | /api/users/:id | الحصول على مستخدم محدد |
| PUT | /api/users/:id | تحديث مستخدم |
| DELETE | /api/users/:id | حذف مستخدم |
| GET | /api/users/:id/profile | الحصول على الملف الشخصي لمستخدم محدد |
| PUT | /api/users/:id/profile | تحديث الملف الشخصي لمستخدم محدد |

#### الدورات

| الطريقة | المسار | الوصف |
|--------|------|--------|
| GET | /api/courses | الحصول على قائمة الدورات |
| GET | /api/courses/:id | الحصول على دورة محددة |
| POST | /api/courses | إنشاء دورة جديدة |
| PUT | /api/courses/:id | تحديث دورة |
| DELETE | /api/courses/:id | حذف دورة |
| GET | /api/courses/:id/lessons | الحصول على دروس دورة محددة |
| POST | /api/courses/:id/enroll | التسجيل في دورة |
| POST | /api/courses/:id/rate | تقييم دورة |

#### الاختبارات

| الطريقة | المسار | الوصف |
|--------|------|--------|
| GET | /api/quizzes | الحصول على قائمة الاختبارات |
| GET | /api/quizzes/:id | الحصول على اختبار محدد |
| POST | /api/quizzes | إنشاء اختبار جديد |
| PUT | /api/quizzes/:id | تحديث اختبار |
| DELETE | /api/quizzes/:id | حذف اختبار |
| GET | /api/quizzes/:id/questions | الحصول على أسئلة اختبار محدد |
| POST | /api/quizzes/:id/attempt | بدء محاولة اختبار |
| POST | /api/quizzes/:id/submit | إرسال إجابات اختبار |

#### أدوات الذكاء الاصطناعي

| الطريقة | المسار | الوصف |
|--------|------|--------|
| GET | /api/ai-tools | الحصول على قائمة أدوات الذكاء الاصطناعي |
| GET | /api/ai-tools/:id | الحصول على أداة ذكاء اصطناعي محددة |
| POST | /api/ai-tools/generate-code | توليد كود |
| POST | /api/ai-tools/explain-code | شرح كود |
| POST | /api/ai-tools/fix-code | تصحيح أخطاء في الكود |
| POST | /api/ai-tools/translate-code | تحويل الكود بين لغات البرمجة |

#### الألعاب

| الطريقة | المسار | الوصف |
|--------|------|--------|
| GET | /api/games | الحصول على قائمة الألعاب |
| GET | /api/games/:id | الحصول على لعبة محددة |
| POST | /api/games | إنشاء لعبة جديدة |
| PUT | /api/games/:id | تحديث لعبة |
| DELETE | /api/games/:id | حذف لعبة |

#### المقالات

| الطريقة | المسار | الوصف |
|--------|------|--------|
| GET | /api/articles | الحصول على قائمة المقالات |
| GET | /api/articles/:id | الحصول على مقال محدد |
| POST | /api/articles | إنشاء مقال جديد |
| PUT | /api/articles/:id | تحديث مقال |
| DELETE | /api/articles/:id | حذف مقال |

#### المنتديات

| الطريقة | المسار | الوصف |
|--------|------|--------|
| GET | /api/forums | الحصول على قائمة المنتديات |
| GET | /api/forums/:id | الحصول على منتدى محدد |
| GET | /api/forums/:id/topics | الحصول على مواضيع منتدى محدد |
| POST | /api/forums/:id/topics | إنشاء موضوع جديد |
| GET | /api/topics/:id | الحصول على موضوع محدد |
| POST | /api/topics/:id/replies | إضافة رد على موضوع |

#### الأدمن

| الطريقة | المسار | الوصف |
|--------|------|--------|
| GET | /api/admin/dashboard | الحصول على بيانات لوحة التحكم |
| GET | /api/admin/users | الحصول على قائمة المستخدمين |
| PUT | /api/admin/users/:id | تحديث مستخدم |
| DELETE | /api/admin/users/:id | حذف مستخدم |
| GET | /api/admin/courses | الحصول على قائمة الدورات |
| POST | /api/admin/courses | إنشاء دورة جديدة |
| PUT | /api/admin/courses/:id | تحديث دورة |
| DELETE | /api/admin/courses/:id | حذف دورة |

### توثيق API

يتم توثيق API باستخدام Swagger/OpenAPI. يمكن الوصول إلى وثائق API من خلال:

```
http://localhost:5000/api/docs
```

## المصادقة والتفويض

### نظام المصادقة

يستخدم موقع Code Aura نظام مصادقة متعدد الطرق:

1. **المصادقة التقليدية**: باستخدام البريد الإلكتروني وكلمة المرور.
2. **المصادقة عبر OAuth**: باستخدام Google، Facebook، وGitHub.

### توكنات JWT

يتم استخدام توكنات JWT (JSON Web Tokens) للمصادقة. يتم إنشاء توكن عند تسجيل الدخول ويتم إرساله مع كل طلب لاحق للتحقق من هوية المستخدم.

```python
# src/routes/auth.py
from flask_jwt_extended import create_access_token

@auth_bp.route('/login', methods=['POST'])
def login():
    # ...
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'token': access_token,
        'user': user.to_dict()
    }), 200
```

### التفويض

يتم التحقق من صلاحيات المستخدم باستخدام مزخرفات مخصصة:

```python
# src/utils/decorators.py
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

from src.models.user import User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            return jsonify({'message': 'غير مصرح لك بالوصول إلى هذا المورد'}), 403
        
        return fn(*args, **kwargs)
    return wrapper
```

### تكامل OAuth

يتم تنفيذ تكامل OAuth باستخدام مكتبة Authlib:

```python
# src/config/oauth.py
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    
    # إعداد Google OAuth
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    
    # إعداد Facebook OAuth
    oauth.register(
        name='facebook',
        client_id=app.config['FACEBOOK_CLIENT_ID'],
        client_secret=app.config['FACEBOOK_CLIENT_SECRET'],
        access_token_url='https://graph.facebook.com/oauth/access_token',
        authorize_url='https://www.facebook.com/dialog/oauth',
        client_kwargs={'scope': 'email'},
    )
    
    # إعداد GitHub OAuth
    oauth.register(
        name='github',
        client_id=app.config['GITHUB_CLIENT_ID'],
        client_secret=app.config['GITHUB_CLIENT_SECRET'],
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        client_kwargs={'scope': 'user:email'},
    )
```

## تكامل الذكاء الاصطناعي

### تكامل OpenAI API

يستخدم موقع Code Aura واجهة برمجة تطبيقات OpenAI لتوفير ميزات الذكاء الاصطناعي:

```python
# src/services/ai_service.py
import openai
from src.config.config import Config

class AIService:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
    
    def generate_code(self, prompt, language):
        """
        توليد كود من وصف نصي
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"أنت مساعد برمجة محترف. قم بتوليد كود {language} بناءً على الوصف التالي."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"خطأ في توليد الكود: {str(e)}")
            return None
```

### تكامل محرر الأكواد

يتم تكامل محرر الأكواد (Monaco Editor) مع أدوات الذكاء الاصطناعي:

```jsx
// src/components/code-editor/CodeEditor.jsx
import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import { useAI } from '../../hooks/useAI';
import './CodeEditor.css';

const CodeEditor = () => {
  const [code, setCode] = useState('// اكتب الكود هنا');
  const [language, setLanguage] = useState('javascript');
  const { generateCode, explainCode, fixCode, translateCode } = useAI();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');

  const handleEditorChange = (value) => {
    setCode(value);
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const handleGenerateCode = async () => {
    setLoading(true);
    try {
      const prompt = window.prompt('أدخل وصفًا للكود الذي تريد توليده:');
      if (prompt) {
        const generatedCode = await generateCode(prompt, language);
        setCode(generatedCode);
      }
    } catch (error) {
      console.error('خطأ في توليد الكود:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExplainCode = async () => {
    setLoading(true);
    try {
      const explanation = await explainCode(code);
      setResult(explanation);
    } catch (error) {
      console.error('خطأ في شرح الكود:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFixCode = async () => {
    setLoading(true);
    try {
      const fixedCode = await fixCode(code, language);
      setCode(fixedCode);
    } catch (error) {
      console.error('خطأ في تصحيح الكود:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTranslateCode = async () => {
    setLoading(true);
    try {
      const targetLanguage = window.prompt('أدخل لغة البرمجة الهدف:');
      if (targetLanguage) {
        const translatedCode = await translateCode(code, language, targetLanguage);
        setCode(translatedCode);
        setLanguage(targetLanguage.toLowerCase());
      }
    } catch (error) {
      console.error('خطأ في تحويل الكود:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="code-editor-container">
      <div className="code-editor-toolbar">
        <select value={language} onChange={handleLanguageChange}>
          <option value="javascript">JavaScript</option>
          <option value="python">Python</option>
          <option value="java">Java</option>
          <option value="csharp">C#</option>
          <option value="cpp">C++</option>
          <option value="php">PHP</option>
          <option value="ruby">Ruby</option>
          <option value="go">Go</option>
          <option value="typescript">TypeScript</option>
          <option value="sql">SQL</option>
          <option value="html">HTML</option>
          <option value="css">CSS</option>
        </select>
        <button onClick={handleGenerateCode} disabled={loading}>
          توليد الكود
        </button>
        <button onClick={handleExplainCode} disabled={loading}>
          شرح الكود
        </button>
        <button onClick={handleFixCode} disabled={loading}>
          تصحيح الأخطاء
        </button>
        <button onClick={handleTranslateCode} disabled={loading}>
          تحويل الكود
        </button>
      </div>
      <div className="code-editor-main">
        <Editor
          height="70vh"
          language={language}
          value={code}
          onChange={handleEditorChange}
          theme="vs-dark"
          options={{
            minimap: { enabled: true },
            fontSize: 14,
            wordWrap: 'on',
            automaticLayout: true,
            tabSize: 2,
          }}
        />
      </div>
      {result && (
        <div className="code-editor-result">
          <h3>النتيجة:</h3>
          <div className="result-content">{result}</div>
        </div>
      )}
    </div>
  );
};

export default CodeEditor;
```

## اختبار الكود

### اختبارات الباك إند

يتم استخدام pytest لاختبار الباك إند:

```python
# tests/test_auth.py
import pytest
from src.main import create_app
from src.models.database import db
from src.models.user import User

@pytest.fixture
def app():
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    assert b'تم إنشاء المستخدم بنجاح' in response.data

def test_login(client):
    # إنشاء مستخدم للاختبار
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # محاولة تسجيل الدخول
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    assert b'token' in response.data
    assert b'user' in response.data
```

### اختبارات الفرونت إند

يتم استخدام Jest و React Testing Library لاختبار الفرونت إند:

```jsx
// tests/components/auth/LoginForm.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../../src/contexts/AuthContext';
import LoginForm from '../../../src/components/auth/LoginForm';
import authService from '../../../src/services/authService';

// Mock authService
jest.mock('../../../src/services/authService');

describe('LoginForm Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders login form correctly', () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <LoginForm />
        </AuthProvider>
      </BrowserRouter>
    );

    expect(screen.getByLabelText(/البريد الإلكتروني/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/كلمة المرور/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /تسجيل الدخول/i })).toBeInTheDocument();
  });

  test('submits form with valid data', async () => {
    authService.login.mockResolvedValue({
      token: 'fake-token',
      user: { id: 1, username: 'testuser', email: 'test@example.com' }
    });

    render(
      <BrowserRouter>
        <AuthProvider>
          <LoginForm />
        </AuthProvider>
      </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText(/البريد الإلكتروني/i), {
      target: { value: 'test@example.com' }
    });

    fireEvent.change(screen.getByLabelText(/كلمة المرور/i), {
      target: { value: 'password123' }
    });

    fireEvent.click(screen.getByRole('button', { name: /تسجيل الدخول/i }));

    await waitFor(() => {
      expect(authService.login).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });

  test('shows error message on invalid login', async () => {
    authService.login.mockRejectedValue({
      response: { data: { message: 'بيانات الدخول غير صحيحة' } }
    });

    render(
      <BrowserRouter>
        <AuthProvider>
          <LoginForm />
        </AuthProvider>
      </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText(/البريد الإلكتروني/i), {
      target: { value: 'invalid@example.com' }
    });

    fireEvent.change(screen.getByLabelText(/كلمة المرور/i), {
      target: { value: 'wrongpassword' }
    });

    fireEvent.click(screen.getByRole('button', { name: /تسجيل الدخول/i }));

    await waitFor(() => {
      expect(screen.getByText(/بيانات الدخول غير صحيحة/i)).toBeInTheDocument();
    });
  });
});
```

### اختبارات E2E

يتم استخدام Cypress لاختبارات E2E:

```javascript
// cypress/integration/login.spec.js
describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should login successfully with valid credentials', () => {
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 200,
      body: {
        token: 'fake-token',
        user: { id: 1, username: 'testuser', email: 'test@example.com' }
      }
    }).as('loginRequest');

    cy.get('input[name="email"]').type('test@example.com');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();

    cy.wait('@loginRequest');
    cy.url().should('include', '/dashboard');
    cy.contains('مرحبًا، testuser').should('be.visible');
  });

  it('should show error message with invalid credentials', () => {
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 401,
      body: { message: 'بيانات الدخول غير صحيحة' }
    }).as('loginRequest');

    cy.get('input[name="email"]').type('invalid@example.com');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();

    cy.wait('@loginRequest');
    cy.contains('بيانات الدخول غير صحيحة').should('be.visible');
    cy.url().should('include', '/login');
  });
});
```

## النشر والتحديث

### النشر على بيئة الإنتاج

#### 1. إعداد الخوادم

يتم استخدام AWS EC2 لاستضافة الموقع:

```bash
# إنشاء مثيل EC2
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.medium \
  --key-name your-key-pair \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=code-aura-production}]'
```

#### 2. إعداد قاعدة البيانات

يتم استخدام AWS RDS لاستضافة قاعدة البيانات:

```bash
# إنشاء مثيل RDS
aws rds create-db-instance \
  --db-instance-identifier code-aura-db \
  --db-instance-class db.t3.small \
  --engine postgres \
  --master-username admin \
  --master-user-password your-password \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-12345678 \
  --db-subnet-group-name your-subnet-group
```

#### 3. نشر الباك إند

```bash
# الاتصال بالخادم
ssh -i your-key.pem ubuntu@your-server-ip

# إنشاء دليل التطبيق
mkdir -p /var/www/code-aura

# تثبيت التبعيات
sudo apt update
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# إنشاء بيئة افتراضية
cd /var/www/code-aura
python3 -m venv venv
source venv/bin/activate

# استنساخ المستودع
git clone https://github.com/your-organization/code-aura.git .
cd backend

# تثبيت التبعيات
pip install -r requirements.txt

# إنشاء ملف .env
cat > .env << EOF
FLASK_APP=src/main.py
FLASK_ENV=production
DATABASE_URL=postgresql://admin:your-password@your-rds-endpoint:5432/code_aura_db
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
EOF

# تطبيق ترحيلات قاعدة البيانات
flask db upgrade

# إعداد Gunicorn
sudo tee /etc/systemd/system/code-aura.service << EOF
[Unit]
Description=Code Aura Backend
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/code-aura/backend
Environment="PATH=/var/www/code-aura/venv/bin"
ExecStart=/var/www/code-aura/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 src.main:app

[Install]
WantedBy=multi-user.target
EOF

# تفعيل وتشغيل الخدمة
sudo systemctl enable code-aura
sudo systemctl start code-aura

# إعداد Nginx
sudo tee /etc/nginx/sites-available/code-aura << EOF
server {
    listen 80;
    server_name api.codeaura.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# تفعيل موقع Nginx
sudo ln -s /etc/nginx/sites-available/code-aura /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# إعداد شهادة SSL
sudo certbot --nginx -d api.codeaura.com
```

#### 4. نشر الفرونت إند

```bash
# على جهازك المحلي
cd frontend

# بناء التطبيق
npm run build

# نسخ الملفات المبنية إلى الخادم
scp -i your-key.pem -r dist/* ubuntu@your-server-ip:/var/www/code-aura/frontend

# على الخادم
ssh -i your-key.pem ubuntu@your-server-ip

# إعداد Nginx للفرونت إند
sudo tee /etc/nginx/sites-available/code-aura-frontend << EOF
server {
    listen 80;
    server_name codeaura.com www.codeaura.com;
    root /var/www/code-aura/frontend;
    index index.html;

    # تكوين Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_comp_level 6;
    gzip_min_length 1000;

    # تكوين التخزين المؤقت
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    location / {
        try_files \$uri \$uri/ /index.html;
    }
}
EOF

# تفعيل موقع Nginx
sudo ln -s /etc/nginx/sites-available/code-aura-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# إعداد شهادة SSL
sudo certbot --nginx -d codeaura.com -d www.codeaura.com
```

### تحديث التطبيق

#### 1. تحديث الباك إند

```bash
# الاتصال بالخادم
ssh -i your-key.pem ubuntu@your-server-ip

# الانتقال إلى دليل التطبيق
cd /var/www/code-aura/backend

# تحديث الكود من Git
git pull

# تفعيل البيئة الافتراضية
source ../venv/bin/activate

# تحديث التبعيات
pip install -r requirements.txt

# تطبيق ترحيلات قاعدة البيانات
flask db upgrade

# إعادة تشغيل الخدمة
sudo systemctl restart code-aura
```

#### 2. تحديث الفرونت إند

```bash
# على جهازك المحلي
cd frontend

# بناء التطبيق
npm run build

# نسخ الملفات المبنية إلى الخادم
scp -i your-key.pem -r dist/* ubuntu@your-server-ip:/var/www/code-aura/frontend
```

## أفضل الممارسات

### أفضل ممارسات الكود

1. **اتباع مبادئ SOLID**:
   - Single Responsibility Principle: كل صنف له مسؤولية واحدة فقط.
   - Open/Closed Principle: الأصناف مفتوحة للتوسيع، مغلقة للتعديل.
   - Liskov Substitution Principle: يجب أن تكون الأصناف الفرعية قابلة للاستبدال بأصنافها الأساسية.
   - Interface Segregation Principle: العديد من الواجهات المحددة أفضل من واجهة واحدة عامة.
   - Dependency Inversion Principle: الاعتماد على التجريدات، وليس على التنفيذات.

2. **استخدام نمط MVC**:
   - Model: نماذج قاعدة البيانات والمنطق التجاري.
   - View: واجهة المستخدم (الفرونت إند).
   - Controller: مسارات API التي تربط بين النماذج والعرض.

3. **كتابة اختبارات شاملة**:
   - اختبارات الوحدة لاختبار الوظائف الفردية.
   - اختبارات التكامل لاختبار تفاعل المكونات مع بعضها البعض.
   - اختبارات E2E لاختبار تجربة المستخدم الكاملة.

4. **استخدام التعليقات بشكل فعال**:
   - كتابة تعليقات توضيحية للكود المعقد.
   - استخدام docstrings لتوثيق الدوال والصفوف.
   - تجنب التعليقات الزائدة عن الحاجة.

### أفضل ممارسات الأمان

1. **حماية البيانات الحساسة**:
   - تشفير كلمات المرور باستخدام خوارزميات تجزئة قوية.
   - عدم تخزين بيانات حساسة في ملفات التكوين.
   - استخدام متغيرات البيئة لتخزين المفاتيح السرية.

2. **حماية من هجمات الويب الشائعة**:
   - حماية من هجمات XSS باستخدام تنظيف المدخلات.
   - حماية من هجمات CSRF باستخدام توكنات CSRF.
   - حماية من هجمات SQL Injection باستخدام ORM.

3. **تنفيذ المصادقة والتفويض بشكل صحيح**:
   - استخدام توكنات JWT للمصادقة.
   - التحقق من صلاحيات المستخدم قبل الوصول إلى الموارد المحمية.
   - تنفيذ تحديد معدل الطلبات لمنع هجمات القوة الغاشمة.

### أفضل ممارسات الأداء

1. **تحسين أداء قاعدة البيانات**:
   - إنشاء فهارس للأعمدة المستخدمة في عمليات البحث.
   - استخدام التخزين المؤقت لتقليل عدد استعلامات قاعدة البيانات.
   - تحسين الاستعلامات لتقليل وقت التنفيذ.

2. **تحسين أداء الفرونت إند**:
   - استخدام تقسيم الكود لتقليل حجم الحزم الأولية.
   - تحسين تحميل الصور باستخدام تحميل كسول.
   - استخدام التخزين المؤقت للمتصفح لتقليل عدد الطلبات.

3. **تحسين أداء الباك إند**:
   - استخدام التخزين المؤقت للاستجابات المتكررة.
   - استخدام مجمع اتصالات لقاعدة البيانات.
   - تنفيذ معالجة غير متزامنة للمهام الثقيلة.

## استكشاف الأخطاء وإصلاحها

### مشاكل الباك إند الشائعة

1. **مشاكل قاعدة البيانات**:
   - التحقق من اتصال قاعدة البيانات.
   - التحقق من صحة استعلامات SQL.
   - التحقق من تطبيق جميع الترحيلات.

2. **مشاكل المصادقة**:
   - التحقق من صحة توكنات JWT.
   - التحقق من تكوين OAuth.
   - التحقق من صلاحيات المستخدم.

3. **مشاكل API**:
   - التحقق من صحة مسارات API.
   - التحقق من معالجة الأخطاء.
   - التحقق من تنسيق الاستجابات.

### مشاكل الفرونت إند الشائعة

1. **مشاكل العرض**:
   - التحقق من توافق CSS مع المتصفحات المختلفة.
   - التحقق من التصميم المتجاوب على أحجام الشاشات المختلفة.
   - التحقق من تحميل الصور والأصول.

2. **مشاكل JavaScript**:
   - التحقق من أخطاء وحدة التحكم في المتصفح.
   - التحقق من تحميل المكتبات والتبعيات.
   - التحقق من معالجة الأحداث.

3. **مشاكل الاتصال بالباك إند**:
   - التحقق من عناوين URL لنقاط نهاية API.
   - التحقق من رؤوس الطلبات.
   - التحقق من معالجة الاستجابات والأخطاء.

### أدوات استكشاف الأخطاء وإصلاحها

1. **أدوات الباك إند**:
   - سجلات التطبيق للتحقق من الأخطاء.
   - أدوات تصحيح Python مثل pdb.
   - أدوات مراقبة الأداء مثل New Relic أو Datadog.

2. **أدوات الفرونت إند**:
   - أدوات مطوري المتصفح للتحقق من الشبكة والوحدة النمطية والأخطاء.
   - React DevTools للتحقق من مكونات React وحالتها.
   - Redux DevTools للتحقق من حالة Redux.

## الموارد والمراجع

### وثائق API

- [Swagger UI](http://localhost:5000/api/docs): وثائق API التفاعلية.
- [Postman Collection](https://www.postman.com/your-organization/workspace/code-aura): مجموعة Postman لاختبار API.

### مستودعات الكود

- [GitHub - Backend](https://github.com/your-organization/code-aura-backend): مستودع الباك إند.
- [GitHub - Frontend](https://github.com/your-organization/code-aura-frontend): مستودع الفرونت إند.

### أدلة التطوير

- [دليل أسلوب الكود](https://github.com/your-organization/code-aura/wiki/Code-Style-Guide): دليل أسلوب الكود للمشروع.
- [دليل المساهمة](https://github.com/your-organization/code-aura/wiki/Contributing-Guide): دليل المساهمة في المشروع.

### موارد خارجية

- [Flask Documentation](https://flask.palletsprojects.com/): وثائق Flask.
- [React Documentation](https://reactjs.org/docs/getting-started.html): وثائق React.
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/): وثائق SQLAlchemy.
- [OpenAI API Documentation](https://platform.openai.com/docs/): وثائق OpenAI API.

