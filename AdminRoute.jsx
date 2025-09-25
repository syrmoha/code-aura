import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const AdminRoute = ({ children }) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();
  
  // إذا كان التحميل جارياً، يمكن عرض شاشة تحميل
  if (loading) {
    return <div className="loading-spinner">جاري التحميل...</div>;
  }
  
  // إذا لم يكن المستخدم مسجل الدخول، توجيهه إلى صفحة تسجيل الدخول
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: window.location.pathname }} />;
  }
  
  // إذا كان المستخدم مسجل الدخول ولكن ليس أدمن، توجيهه إلى الصفحة الرئيسية
  if (!isAdmin) {
    return <Navigate to="/" />;
  }
  
  // إذا كان المستخدم أدمن، عرض المحتوى المطلوب
  return children;
};

export default AdminRoute;

