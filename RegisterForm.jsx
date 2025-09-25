import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

const RegisterForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [formError, setFormError] = useState('');
  const { register, loading } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const validateForm = () => {
    if (!formData.username || !formData.email || !formData.password || !formData.confirmPassword) {
      setFormError('جميع الحقول مطلوبة');
      return false;
    }

    if (formData.password !== formData.confirmPassword) {
      setFormError('كلمات المرور غير متطابقة');
      return false;
    }

    if (formData.password.length < 8) {
      setFormError('يجب أن تتكون كلمة المرور من 8 أحرف على الأقل');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    
    if (!validateForm()) {
      return;
    }
    
    try {
      await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
      });
      navigate('/login', { state: { message: 'تم إنشاء الحساب بنجاح. يرجى تسجيل الدخول.' } });
    } catch (error) {
      console.error('Registration error:', error);
      setFormError(error.response?.data?.message || 'فشل التسجيل. يرجى المحاولة مرة أخرى.');
    }
  };

  return (
    <div className="register-form-container">
      <div className="form-wrapper">
        <h2 className="form-title">إنشاء حساب جديد</h2>
        
        {formError && (
          <div className="error-message">
            {formError}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="register-form">
          <div className="form-group">
            <label htmlFor="username">اسم المستخدم</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="أدخل اسم المستخدم"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">البريد الإلكتروني</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="أدخل بريدك الإلكتروني"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">كلمة المرور</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="أدخل كلمة المرور"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="confirmPassword">تأكيد كلمة المرور</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="أعد إدخال كلمة المرور"
              required
            />
          </div>
          
          <div className="form-actions">
            <button 
              type="submit" 
              className="register-button"
              disabled={loading}
            >
              {loading ? 'جاري التسجيل...' : 'إنشاء حساب'}
            </button>
          </div>
          
          <div className="form-links">
            <div className="login-link">
              لديك حساب بالفعل؟ <Link to="/login">تسجيل الدخول</Link>
            </div>
          </div>
        </form>
        
        <div className="social-register">
          <p className="social-register-title">أو التسجيل باستخدام</p>
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

export default RegisterForm;

