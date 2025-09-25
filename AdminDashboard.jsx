import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/api';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    users: 0,
    courses: 0,
    quizzes: 0,
    games: 0,
    aiTools: 0,
    articles: 0,
    forums: 0,
    categories: 0
  });
  
  const [recentUsers, setRecentUsers] = useState([]);
  const [recentCourses, setRecentCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // في الإنتاج، استخدم API حقيقي
      // const response = await adminService.getDashboardStats();
      
      // بيانات تجريبية للعرض
      const mockStats = {
        users: 156,
        courses: 13,
        quizzes: 25,
        games: 5,
        aiTools: 5,
        articles: 12,
        forums: 8,
        categories: 10
      };
      
      const mockRecentUsers = [
        { id: 1, username: 'أحمد محمد', email: 'ahmed@example.com', created_at: '2023-09-20', role: 'مستخدم' },
        { id: 2, username: 'سارة علي', email: 'sara@example.com', created_at: '2023-09-19', role: 'مستخدم' },
        { id: 3, username: 'محمد خالد', email: 'mohamed@example.com', created_at: '2023-09-18', role: 'مستخدم' },
        { id: 4, username: 'فاطمة أحمد', email: 'fatima@example.com', created_at: '2023-09-17', role: 'مستخدم' },
        { id: 5, username: 'عمر حسن', email: 'omar@example.com', created_at: '2023-09-16', role: 'مستخدم' }
      ];
      
      const mockRecentCourses = [
        { id: 1, title: 'دورة Python للمبتدئين', language: 'عربية', created_at: '2023-09-20', views: 120 },
        { id: 2, title: 'تعلم JavaScript من الصفر', language: 'عربية', created_at: '2023-09-19', views: 95 },
        { id: 3, title: 'دورة React المتقدمة', language: 'عربية', created_at: '2023-09-18', views: 85 },
        { id: 4, title: 'أساسيات قواعد البيانات SQL', language: 'عربية', created_at: '2023-09-17', views: 70 },
        { id: 5, title: 'تطوير تطبيقات الويب الحديثة', language: 'عربية', created_at: '2023-09-16', views: 65 }
      ];
      
      setStats(mockStats);
      setRecentUsers(mockRecentUsers);
      setRecentCourses(mockRecentCourses);
      
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('حدث خطأ أثناء تحميل بيانات لوحة المعلومات');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="dashboard-loading">جاري تحميل البيانات...</div>;
  }

  if (error) {
    return <div className="dashboard-error">{error}</div>;
  }

  return (
    <div className="admin-dashboard">
      <h2 className="dashboard-title">لوحة المعلومات</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon users">
            <i className="fas fa-users"></i>
          </div>
          <div className="stat-info">
            <h3>المستخدمين</h3>
            <p className="stat-value">{stats.users}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon courses">
            <i className="fas fa-graduation-cap"></i>
          </div>
          <div className="stat-info">
            <h3>الدورات</h3>
            <p className="stat-value">{stats.courses}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon quizzes">
            <i className="fas fa-question-circle"></i>
          </div>
          <div className="stat-info">
            <h3>الاختبارات</h3>
            <p className="stat-value">{stats.quizzes}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon games">
            <i className="fas fa-gamepad"></i>
          </div>
          <div className="stat-info">
            <h3>الألعاب</h3>
            <p className="stat-value">{stats.games}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon ai-tools">
            <i className="fas fa-robot"></i>
          </div>
          <div className="stat-info">
            <h3>أدوات الذكاء الاصطناعي</h3>
            <p className="stat-value">{stats.aiTools}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon articles">
            <i className="fas fa-newspaper"></i>
          </div>
          <div className="stat-info">
            <h3>المقالات</h3>
            <p className="stat-value">{stats.articles}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon forums">
            <i className="fas fa-comments"></i>
          </div>
          <div className="stat-info">
            <h3>المنتديات</h3>
            <p className="stat-value">{stats.forums}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon categories">
            <i className="fas fa-tags"></i>
          </div>
          <div className="stat-info">
            <h3>التصنيفات</h3>
            <p className="stat-value">{stats.categories}</p>
          </div>
        </div>
      </div>
      
      <div className="dashboard-row">
        <div className="dashboard-card recent-users">
          <div className="card-header">
            <h3>أحدث المستخدمين</h3>
            <button className="view-all-button">عرض الكل</button>
          </div>
          
          <div className="card-content">
            <table className="data-table">
              <thead>
                <tr>
                  <th>اسم المستخدم</th>
                  <th>البريد الإلكتروني</th>
                  <th>تاريخ التسجيل</th>
                  <th>الدور</th>
                </tr>
              </thead>
              <tbody>
                {recentUsers.map(user => (
                  <tr key={user.id}>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                    <td>{user.created_at}</td>
                    <td>{user.role}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        
        <div className="dashboard-card recent-courses">
          <div className="card-header">
            <h3>أحدث الدورات</h3>
            <button className="view-all-button">عرض الكل</button>
          </div>
          
          <div className="card-content">
            <table className="data-table">
              <thead>
                <tr>
                  <th>عنوان الدورة</th>
                  <th>اللغة</th>
                  <th>تاريخ الإضافة</th>
                  <th>المشاهدات</th>
                </tr>
              </thead>
              <tbody>
                {recentCourses.map(course => (
                  <tr key={course.id}>
                    <td>{course.title}</td>
                    <td>{course.language}</td>
                    <td>{course.created_at}</td>
                    <td>{course.views}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      <div className="dashboard-row">
        <div className="dashboard-card quick-actions">
          <div className="card-header">
            <h3>إجراءات سريعة</h3>
          </div>
          
          <div className="card-content">
            <div className="quick-actions-grid">
              <button className="quick-action-button">
                <i className="fas fa-user-plus"></i>
                <span>إضافة مستخدم</span>
              </button>
              
              <button className="quick-action-button">
                <i className="fas fa-plus-circle"></i>
                <span>إضافة دورة</span>
              </button>
              
              <button className="quick-action-button">
                <i className="fas fa-plus-square"></i>
                <span>إضافة اختبار</span>
              </button>
              
              <button className="quick-action-button">
                <i className="fas fa-edit"></i>
                <span>كتابة مقال</span>
              </button>
              
              <button className="quick-action-button">
                <i className="fas fa-cog"></i>
                <span>إعدادات الموقع</span>
              </button>
              
              <button className="quick-action-button">
                <i className="fas fa-database"></i>
                <span>نسخ احتياطي</span>
              </button>
            </div>
          </div>
        </div>
        
        <div className="dashboard-card system-info">
          <div className="card-header">
            <h3>معلومات النظام</h3>
          </div>
          
          <div className="card-content">
            <div className="system-info-item">
              <span className="info-label">إصدار النظام:</span>
              <span className="info-value">Code Aura v1.0.0</span>
            </div>
            
            <div className="system-info-item">
              <span className="info-label">آخر تحديث:</span>
              <span className="info-value">25 سبتمبر 2023</span>
            </div>
            
            <div className="system-info-item">
              <span className="info-label">حالة الخادم:</span>
              <span className="info-value status-ok">متصل</span>
            </div>
            
            <div className="system-info-item">
              <span className="info-label">استخدام التخزين:</span>
              <div className="progress-bar">
                <div className="progress" style={{ width: '45%' }}></div>
              </div>
              <span className="progress-text">45% (450MB / 1GB)</span>
            </div>
            
            <div className="system-info-item">
              <span className="info-label">استخدام المعالج:</span>
              <div className="progress-bar">
                <div className="progress" style={{ width: '30%' }}></div>
              </div>
              <span className="progress-text">30%</span>
            </div>
            
            <div className="system-info-item">
              <span className="info-label">استخدام الذاكرة:</span>
              <div className="progress-bar">
                <div className="progress" style={{ width: '60%' }}></div>
              </div>
              <span className="progress-text">60% (1.2GB / 2GB)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;

