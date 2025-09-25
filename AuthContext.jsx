import React, { createContext, useState, useEffect, useContext } from 'react';
import { authService } from '../services/api';

// إنشاء سياق المصادقة
const AuthContext = createContext();

// مزود سياق المصادقة
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // التحقق من وجود مستخدم مسجل الدخول عند تحميل التطبيق
  useEffect(() => {
    const user = authService.getCurrentUser();
    if (user) {
      setCurrentUser(user);
    }
    setLoading(false);
  }, []);

  // تسجيل الدخول باستخدام البريد الإلكتروني وكلمة المرور
  const login = async (email, password) => {
    try {
      setError(null);
      setLoading(true);
      const data = await authService.login(email, password);
      setCurrentUser(data.user);
      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'حدث خطأ أثناء تسجيل الدخول');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // تسجيل مستخدم جديد
  const register = async (userData) => {
    try {
      setError(null);
      setLoading(true);
      const data = await authService.register(userData);
      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'حدث خطأ أثناء التسجيل');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // تسجيل الخروج
  const logout = () => {
    authService.logout();
    setCurrentUser(null);
  };

  // تسجيل الدخول باستخدام Google
  const googleLogin = async (tokenId) => {
    try {
      setError(null);
      setLoading(true);
      const data = await authService.googleLogin(tokenId);
      setCurrentUser(data.user);
      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'حدث خطأ أثناء تسجيل الدخول باستخدام Google');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // تسجيل الدخول باستخدام Facebook
  const facebookLogin = async (accessToken) => {
    try {
      setError(null);
      setLoading(true);
      const data = await authService.facebookLogin(accessToken);
      setCurrentUser(data.user);
      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'حدث خطأ أثناء تسجيل الدخول باستخدام Facebook');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // تسجيل الدخول باستخدام GitHub
  const githubLogin = async (code) => {
    try {
      setError(null);
      setLoading(true);
      const data = await authService.githubLogin(code);
      setCurrentUser(data.user);
      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'حدث خطأ أثناء تسجيل الدخول باستخدام GitHub');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // تحديث معلومات المستخدم
  const updateProfile = async (userData) => {
    try {
      setError(null);
      setLoading(true);
      const data = await authService.updateUserProfile(userData);
      setCurrentUser({ ...currentUser, ...data.user });
      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'حدث خطأ أثناء تحديث الملف الشخصي');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // تغيير كلمة المرور
  const changePassword = async (currentPassword, newPassword) => {
    try {
      setError(null);
      setLoading(true);
      const data = await authService.changePassword(currentPassword, newPassword);
      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'حدث خطأ أثناء تغيير كلمة المرور');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // القيمة التي سيتم توفيرها للمكونات
  const value = {
    currentUser,
    loading,
    error,
    login,
    register,
    logout,
    googleLogin,
    facebookLogin,
    githubLogin,
    updateProfile,
    changePassword,
    isAuthenticated: !!currentUser,
    isAdmin: currentUser?.role === 'admin'
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// هوك مخصص لاستخدام سياق المصادقة
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth يجب استخدامه داخل AuthProvider');
  }
  return context;
};

export default AuthContext;

