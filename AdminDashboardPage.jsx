import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { adminService } from '../../services/api';
import AdminDashboard from './AdminDashboard';
import AdminUsers from './AdminUsers';
import AdminCourses from './AdminCourses';
import AdminQuizzes from './AdminQuizzes';
import AdminGames from './AdminGames';
import AdminAITools from './AdminAITools';
import AdminArticles from './AdminArticles';
import AdminForums from './AdminForums';
import AdminCategories from './AdminCategories';
import AdminHomeSettings from './AdminHomeSettings';
import './AdminDashboardPage.css';

const AdminDashboardPage = () => {
  const { currentUser, isAdmin, isAuthenticated } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // التحقق من صلاحيات الأدمن
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/admin' } });
      return;
    }
    
    if (!isAdmin) {
      navigate('/');
      return;
    }
    
    setLoading(false);
  }, [isAuthenticated, isAdmin, navigate]);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  if (loading) {
    return <div className="admin-loading">جاري التحميل...</div>;
  }

  return (
    <div className={`admin-dashboard-page ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
      <div className="admin-sidebar">
        <div className="sidebar-header">
          <h2>لوحة التحكم</h2>
          <button className="sidebar-toggle" onClick={toggleSidebar}>
            <i className={`fas ${sidebarOpen ? 'fa-chevron-right' : 'fa-chevron-left'}`}></i>
          </button>
        </div>
        
        <div className="admin-profile">
          <div className="admin-avatar">
            <i className="fas fa-user-shield"></i>
          </div>
          <div className="admin-info">
            <h3>{currentUser?.username || 'أدمن'}</h3>
            <p>{currentUser?.email}</p>
          </div>
        </div>
        
        <nav className="admin-nav">
          <ul>
            <li>
              <Link to="/admin" className={window.location.pathname === '/admin' ? 'active' : ''}>
                <i className="fas fa-tachometer-alt"></i>
                <span>لوحة المعلومات</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/users" className={window.location.pathname.includes('/admin/users') ? 'active' : ''}>
                <i className="fas fa-users"></i>
                <span>المستخدمين</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/courses" className={window.location.pathname.includes('/admin/courses') ? 'active' : ''}>
                <i className="fas fa-graduation-cap"></i>
                <span>الدورات</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/quizzes" className={window.location.pathname.includes('/admin/quizzes') ? 'active' : ''}>
                <i className="fas fa-question-circle"></i>
                <span>الاختبارات</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/games" className={window.location.pathname.includes('/admin/games') ? 'active' : ''}>
                <i className="fas fa-gamepad"></i>
                <span>الألعاب</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/ai-tools" className={window.location.pathname.includes('/admin/ai-tools') ? 'active' : ''}>
                <i className="fas fa-robot"></i>
                <span>أدوات الذكاء الاصطناعي</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/articles" className={window.location.pathname.includes('/admin/articles') ? 'active' : ''}>
                <i className="fas fa-newspaper"></i>
                <span>المقالات</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/forums" className={window.location.pathname.includes('/admin/forums') ? 'active' : ''}>
                <i className="fas fa-comments"></i>
                <span>المنتديات</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/categories" className={window.location.pathname.includes('/admin/categories') ? 'active' : ''}>
                <i className="fas fa-tags"></i>
                <span>التصنيفات</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/home-settings" className={window.location.pathname.includes('/admin/home-settings') ? 'active' : ''}>
                <i className="fas fa-home"></i>
                <span>إعدادات الصفحة الرئيسية</span>
              </Link>
            </li>
          </ul>
        </nav>
        
        <div className="sidebar-footer">
          <Link to="/" className="view-site">
            <i className="fas fa-external-link-alt"></i>
            <span>عرض الموقع</span>
          </Link>
          <button className="logout-button">
            <i className="fas fa-sign-out-alt"></i>
            <span>تسجيل الخروج</span>
          </button>
        </div>
      </div>
      
      <div className="admin-content">
        <div className="admin-header">
          <div className="header-left">
            <button className="mobile-sidebar-toggle" onClick={toggleSidebar}>
              <i className="fas fa-bars"></i>
            </button>
            <h1>لوحة تحكم الأدمن</h1>
          </div>
          
          <div className="header-right">
            <div className="search-box">
              <input type="text" placeholder="بحث..." />
              <i className="fas fa-search"></i>
            </div>
            
            <div className="header-actions">
              <button className="notification-button">
                <i className="fas fa-bell"></i>
                <span className="notification-badge">3</span>
              </button>
              
              <div className="admin-dropdown">
                <button className="admin-dropdown-toggle">
                  <i className="fas fa-user-circle"></i>
                  <span>{currentUser?.username || 'أدمن'}</span>
                  <i className="fas fa-chevron-down"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div className="admin-content-body">
          <Routes>
            <Route path="/" element={<AdminDashboard />} />
            <Route path="/users/*" element={<AdminUsers />} />
            <Route path="/courses/*" element={<AdminCourses />} />
            <Route path="/quizzes/*" element={<AdminQuizzes />} />
            <Route path="/games/*" element={<AdminGames />} />
            <Route path="/ai-tools/*" element={<AdminAITools />} />
            <Route path="/articles/*" element={<AdminArticles />} />
            <Route path="/forums/*" element={<AdminForums />} />
            <Route path="/categories/*" element={<AdminCategories />} />
            <Route path="/home-settings" element={<AdminHomeSettings />} />
            <Route path="*" element={<Navigate to="/admin" replace />} />
          </Routes>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboardPage;

