import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  // إذا كان التحميل جارياً، يمكن عرض شاشة تحميل
  if (loading) {
    return <div className="loading-spinner">جاري التحميل...</div>;
  }
  
  // إذا لم يكن المستخدم مسجل الدخول، توجيهه إلى صفحة تسجيل الدخول
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: window.location.pathname }} />;
  }
  
  // إذا كان المستخدم مسجل الدخول، عرض المحتوى المطلوب
  return children;
};

export default PrivateRoute;

