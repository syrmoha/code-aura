import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { aiToolService } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import './AIToolDetail.css';

const AIToolDetail = () => {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const [tool, setTool] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('javascript');
  const [targetLanguage, setTargetLanguage] = useState('python');
  const [result, setResult] = useState(null);
  const [processing, setProcessing] = useState(false);

  // قائمة اللغات المدعومة
  const supportedLanguages = [
    { id: 'javascript', name: 'JavaScript' },
    { id: 'python', name: 'Python' },
    { id: 'java', name: 'Java' },
    { id: 'csharp', name: 'C#' },
    { id: 'cpp', name: 'C++' },
    { id: 'php', name: 'PHP' },
    { id: 'ruby', name: 'Ruby' },
    { id: 'go', name: 'Go' },
    { id: 'sql', name: 'SQL' },
  ];

  useEffect(() => {
    fetchToolDetails();
  }, [id]);

  const fetchToolDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await aiToolService.getToolById(id);
      setTool(response);
      
      // تعيين قيم افتراضية بناءً على نوع الأداة
      if (response.tool_type === 'generate_code') {
        setPrompt('إنشاء دالة لحساب مجموع عناصر مصفوفة');
      } else if (response.tool_type === 'debug_code') {
        setCode('function calculateSum(arr) {\n  let sum = 0;\n  for (let i = 0; i < arr.length; i++) {\n    sum += arr[i];\n  }\n  return sum\n}');
      } else if (response.tool_type === 'explain_code') {
        setCode('function factorial(n) {\n  if (n <= 1) return 1;\n  return n * factorial(n - 1);\n}');
      } else if (response.tool_type === 'convert_code') {
        setCode('function greet(name) {\n  return `Hello, ${name}!`;\n}');
      }
      
    } catch (err) {
      console.error('Error fetching tool details:', err);
      setError('حدث خطأ أثناء تحميل تفاصيل الأداة. يرجى المحاولة مرة أخرى.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      setError('يجب تسجيل الدخول لاستخدام أدوات الذكاء الاصطناعي');
      return;
    }
    
    try {
      setProcessing(true);
      setResult(null);
      
      const requestData = {
        prompt: prompt,
        code: code,
        language: language
      };
      
      if (tool.tool_type === 'convert_code') {
        requestData.target_language = targetLanguage;
      }
      
      const response = await aiToolService.useAITool(id, requestData);
      setResult(response);
      
    } catch (err) {
      console.error('Error using AI tool:', err);
      setError('حدث خطأ أثناء استخدام الأداة. يرجى المحاولة مرة أخرى.');
    } finally {
      setProcessing(false);
    }
  };

  // تحديد أيقونة نوع الأداة
  const getToolTypeIcon = (type) => {
    switch (type) {
      case 'generate_code':
        return 'fas fa-code';
      case 'debug_code':
        return 'fas fa-bug';
      case 'explain_code':
        return 'fas fa-book-open';
      case 'convert_code':
        return 'fas fa-exchange-alt';
      default:
        return 'fas fa-robot';
    }
  };
  
  // ترجمة نوع الأداة إلى العربية
  const translateToolType = (type) => {
    switch (type) {
      case 'generate_code':
        return 'توليد الكود';
      case 'debug_code':
        return 'تصحيح الأخطاء';
      case 'explain_code':
        return 'شرح الكود';
      case 'convert_code':
        return 'تحويل الكود';
      default:
        return type;
    }
  };

  if (loading) {
    return <div className="loading-spinner">جاري تحميل تفاصيل الأداة...</div>;
  }

  if (error && !tool) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="ai-tool-detail">
      <div className="tool-header">
        <div className="tool-icon">
          <i className={getToolTypeIcon(tool.tool_type)}></i>
        </div>
        <div className="tool-info">
          <h1>{tool.name}</h1>
          <div className="tool-type">{translateToolType(tool.tool_type)}</div>
          <p className="tool-description">{tool.description}</p>
        </div>
      </div>
      
      {!isAuthenticated && (
        <div className="auth-message">
          <p>
            <i className="fas fa-lock"></i>
            يجب <Link to="/login">تسجيل الدخول</Link> لاستخدام أدوات الذكاء الاصطناعي
          </p>
        </div>
      )}
      
      {error && (
        <div className="error-message">
          <i className="fas fa-exclamation-circle"></i> {error}
        </div>
      )}
      
      <div className="tool-form-container">
        <form onSubmit={handleSubmit} className="tool-form">
          {tool.tool_type === 'generate_code' && (
            <>
              <div className="form-group">
                <label htmlFor="prompt">وصف الكود المطلوب:</label>
                <textarea
                  id="prompt"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="اكتب وصفاً للكود الذي تريد إنشاءه..."
                  required
                  rows={4}
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="language">لغة البرمجة:</label>
                <select
                  id="language"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                >
                  {supportedLanguages.map((lang) => (
                    <option key={lang.id} value={lang.id}>
                      {lang.name}
                    </option>
                  ))}
                </select>
              </div>
            </>
          )}
          
          {(tool.tool_type === 'debug_code' || tool.tool_type === 'explain_code' || tool.tool_type === 'convert_code') && (
            <>
              <div className="form-group">
                <label htmlFor="code">الكود:</label>
                <textarea
                  id="code"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="اكتب أو الصق الكود هنا..."
                  required
                  rows={10}
                  className="code-textarea"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="language">لغة البرمجة:</label>
                <select
                  id="language"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                >
                  {supportedLanguages.map((lang) => (
                    <option key={lang.id} value={lang.id}>
                      {lang.name}
                    </option>
                  ))}
                </select>
              </div>
            </>
          )}
          
          {tool.tool_type === 'debug_code' && (
            <div className="form-group">
              <label htmlFor="prompt">وصف المشكلة (اختياري):</label>
              <textarea
                id="prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="اكتب وصفاً للمشكلة التي تواجهها في الكود..."
                rows={2}
              />
            </div>
          )}
          
          {tool.tool_type === 'convert_code' && (
            <div className="form-group">
              <label htmlFor="targetLanguage">اللغة المستهدفة:</label>
              <select
                id="targetLanguage"
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
              >
                {supportedLanguages
                  .filter((lang) => lang.id !== language)
                  .map((lang) => (
                    <option key={lang.id} value={lang.id}>
                      {lang.name}
                    </option>
                  ))}
              </select>
            </div>
          )}
          
          <button
            type="submit"
            className="submit-button"
            disabled={processing || !isAuthenticated}
          >
            {processing ? (
              <>
                <i className="fas fa-spinner fa-spin"></i> جاري المعالجة...
              </>
            ) : (
              <>
                <i className={getToolTypeIcon(tool.tool_type)}></i>
                {tool.tool_type === 'generate_code' && 'توليد الكود'}
                {tool.tool_type === 'debug_code' && 'تصحيح الأخطاء'}
                {tool.tool_type === 'explain_code' && 'شرح الكود'}
                {tool.tool_type === 'convert_code' && 'تحويل الكود'}
              </>
            )}
          </button>
        </form>
      </div>
      
      {result && (
        <div className="result-container">
          <h2>النتيجة</h2>
          
          {tool.tool_type === 'generate_code' && result.generated_code && (
            <div className="result-code">
              <h3>الكود المولد:</h3>
              <pre>{result.generated_code}</pre>
              <button
                className="copy-button"
                onClick={() => {
                  navigator.clipboard.writeText(result.generated_code);
                  alert('تم نسخ الكود إلى الحافظة');
                }}
              >
                <i className="fas fa-copy"></i> نسخ الكود
              </button>
            </div>
          )}
          
          {tool.tool_type === 'debug_code' && result.debug_result && (
            <div className="result-debug">
              <h3>نتائج التصحيح:</h3>
              <div className="debug-result">{result.debug_result}</div>
            </div>
          )}
          
          {tool.tool_type === 'explain_code' && result.explanation && (
            <div className="result-explanation">
              <h3>شرح الكود:</h3>
              <div className="explanation">{result.explanation}</div>
            </div>
          )}
          
          {tool.tool_type === 'convert_code' && result.converted_code && (
            <div className="result-code">
              <h3>الكود المحول ({result.target_language}):</h3>
              <pre>{result.converted_code}</pre>
              <button
                className="copy-button"
                onClick={() => {
                  navigator.clipboard.writeText(result.converted_code);
                  alert('تم نسخ الكود إلى الحافظة');
                }}
              >
                <i className="fas fa-copy"></i> نسخ الكود
              </button>
            </div>
          )}
        </div>
      )}
      
      <div className="tool-tips">
        <h3>نصائح لاستخدام {tool.name}</h3>
        <ul>
          {tool.tool_type === 'generate_code' && (
            <>
              <li>كن محدداً في وصف الكود الذي تريده للحصول على نتائج أفضل</li>
              <li>حدد المدخلات والمخرجات المتوقعة في وصفك</li>
              <li>اذكر أي متطلبات خاصة مثل الأداء أو الذاكرة</li>
            </>
          )}
          
          {tool.tool_type === 'debug_code' && (
            <>
              <li>تأكد من تضمين الكود الكامل للحصول على تحليل دقيق</li>
              <li>وصف المشكلة بوضوح يساعد في تحديد الأخطاء بشكل أفضل</li>
              <li>قم بتجربة الحلول المقترحة وتعديلها حسب الحاجة</li>
            </>
          )}
          
          {tool.tool_type === 'explain_code' && (
            <>
              <li>قدم كوداً كاملاً قدر الإمكان للحصول على شرح شامل</li>
              <li>للأكواد الطويلة، قم بتقسيمها إلى أجزاء أصغر لشرح كل جزء على حدة</li>
              <li>استخدم الشرح لفهم الخوارزميات المعقدة وتحسين مهاراتك</li>
            </>
          )}
          
          {tool.tool_type === 'convert_code' && (
            <>
              <li>تأكد من أن الكود المصدر يعمل بشكل صحيح قبل التحويل</li>
              <li>قد تحتاج إلى تعديل الكود المحول لمراعاة اختلافات اللغات</li>
              <li>بعض الميزات الخاصة بلغة معينة قد لا يكون لها مكافئ مباشر في لغات أخرى</li>
            </>
          )}
        </ul>
      </div>
      
      <div className="related-tools">
        <h3>أدوات ذكاء اصطناعي أخرى</h3>
        <div className="related-tools-links">
          <Link to="/ai-tools" className="related-tool-link">
            <i className="fas fa-th-list"></i> جميع الأدوات
          </Link>
          <Link to="/code-editor" className="related-tool-link">
            <i className="fas fa-code"></i> محرر الأكواد
          </Link>
        </div>
      </div>
    </div>
  );
};

export default AIToolDetail;

