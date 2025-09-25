import React from 'react';
import { Helmet } from 'react-helmet-async';
import CodeEditor from '../components/code-editor/CodeEditor';
import './CodeEditorPage.css';

const CodeEditorPage = () => {
  return (
    <div className="code-editor-page">
      <Helmet>
        <title>محرر الأكواد | Code Aura</title>
        <meta name="description" content="محرر أكواد متقدم مع دعم الذكاء الاصطناعي لتوليد وتصحيح وشرح وتحويل الكود" />
      </Helmet>
      
      <div className="page-header">
        <h1>محرر الأكواد</h1>
        <p className="page-description">
          محرر أكواد متقدم مع دعم الذكاء الاصطناعي لمساعدتك في كتابة وتحسين الكود
        </p>
      </div>
      
      <div className="editor-features">
        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-code"></i>
          </div>
          <h3>إبراز بناء الجملة</h3>
          <p>دعم لأكثر من 15 لغة برمجة مع إبراز بناء الجملة</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-robot"></i>
          </div>
          <h3>توليد الكود</h3>
          <p>استخدم الذكاء الاصطناعي لتوليد الكود بناءً على وصف بسيط</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-bug"></i>
          </div>
          <h3>تصحيح الأخطاء</h3>
          <p>اكتشاف وتصحيح الأخطاء في الكود تلقائياً</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">
            <i className="fas fa-book"></i>
          </div>
          <h3>شرح الكود</h3>
          <p>الحصول على شرح مفصل للكود بلغة بسيطة</p>
        </div>
      </div>
      
      <CodeEditor />
      
      <div className="editor-tips">
        <h2>نصائح لاستخدام المحرر</h2>
        <ul>
          <li>
            <strong>الإكمال التلقائي:</strong> اضغط على <code>Ctrl+Space</code> لعرض اقتراحات الإكمال التلقائي
          </li>
          <li>
            <strong>تنسيق الكود:</strong> اضغط على <code>Shift+Alt+F</code> لتنسيق الكود تلقائياً
          </li>
          <li>
            <strong>البحث:</strong> اضغط على <code>Ctrl+F</code> للبحث في الكود
          </li>
          <li>
            <strong>الاستبدال:</strong> اضغط على <code>Ctrl+H</code> للبحث والاستبدال
          </li>
          <li>
            <strong>التعليقات:</strong> اضغط على <code>Ctrl+/</code> لإضافة/إزالة تعليق على السطر الحالي
          </li>
        </ul>
      </div>
      
      <div className="ai-tools-info">
        <h2>أدوات الذكاء الاصطناعي</h2>
        <div className="ai-tools-grid">
          <div className="ai-tool-info-card">
            <h3>توليد الكود</h3>
            <p>
              أدخل وصفاً لما تريد إنشاءه، وسيقوم الذكاء الاصطناعي بتوليد الكود المناسب.
              مثال: "إنشاء دالة لحساب مجموع عناصر مصفوفة"
            </p>
          </div>
          
          <div className="ai-tool-info-card">
            <h3>تصحيح الأخطاء</h3>
            <p>
              اكتب الكود الذي يحتوي على أخطاء، وسيقوم الذكاء الاصطناعي بتحديد الأخطاء واقتراح التصحيحات.
            </p>
          </div>
          
          <div className="ai-tool-info-card">
            <h3>شرح الكود</h3>
            <p>
              اكتب أو الصق الكود الذي تريد فهمه، وسيقوم الذكاء الاصطناعي بتقديم شرح مفصل له.
            </p>
          </div>
          
          <div className="ai-tool-info-card">
            <h3>تحويل الكود</h3>
            <p>
              اكتب الكود بلغة برمجة معينة، ثم اختر اللغة المستهدفة، وسيقوم الذكاء الاصطناعي بتحويل الكود.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodeEditorPage;

