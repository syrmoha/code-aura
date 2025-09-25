import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState('');
  const { login, loading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    
    if (!email || !password) {
      setFormError('يرجى إدخال البريد الإلكتروني وكلمة المرور');
      return;
    }
    
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      setFormError(error.response?.data?.message || 'فشل تسجيل الدخول. يرجى التحقق من بيانات الاعتماد الخاصة بك.');
    }
  };

  return (
    <div className="login-form-container">
      <div className="form-wrapper">
        <h2 className="form-title">تسجيل الدخول</h2>
        
        {formError && (
          <div className="error-message">
            {formError}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">البريد الإلكتروني</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="أدخل بريدك الإلكتروني"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">كلمة المرور</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="أدخل كلمة المرور"
              required
            />
          </div>
          
          <div className="form-actions">
            <button 
              type="submit" 
              className="login-button"
              disabled={loading}
            >
              {loading ? 'جاري تسجيل الدخول...' : 'تسجيل الدخول'}
            </button>
          </div>
          
          <div className="form-links">
            <Link to="/forgot-password" className="forgot-password-link">
              نسيت كلمة المرور؟
            </Link>
            <div className="register-link">
              ليس لديك حساب؟ <Link to="/register">إنشاء حساب جديد</Link>
            </div>
          </div>
        </form>
        
        <div className="social-login">
          <p className="social-login-title">أو تسجيل الدخول باستخدام</p>
          <div className="social-buttons">
            <button className="social-button google">
              <i className="fab fa-google"></i> Google
            </button>
            <button className="social-button facebook">
              <i className="fab fa-facebook-f"></i> Facebook
            </button>
            <button className="social-button github">
              <i className="fab fa-github"></i> GitHub
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;

