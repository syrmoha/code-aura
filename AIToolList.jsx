import React, { useState, useEffect } from 'react';
import { aiToolService } from '../../services/api';
import AIToolCard from './AIToolCard';

const AIToolList = () => {
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeFilter, setActiveFilter] = useState('all');

  useEffect(() => {
    fetchTools();
  }, []);

  const fetchTools = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await aiToolService.getAllTools();
      setTools(response.tools);
    } catch (err) {
      console.error('Error fetching AI tools:', err);
      setError('حدث خطأ أثناء تحميل أدوات الذكاء الاصطناعي. يرجى المحاولة مرة أخرى.');
    } finally {
      setLoading(false);
    }
  };

  const filterTools = (tools) => {
    if (activeFilter === 'all') {
      return tools;
    }
    return tools.filter(tool => tool.tool_type === activeFilter);
  };

  const handleFilterChange = (filter) => {
    setActiveFilter(filter);
  };

  // ترجمة نوع الأداة إلى العربية
  const translateToolType = (type) => {
    switch (type) {
      case 'all':
        return 'جميع الأدوات';
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

  const filteredTools = filterTools(tools);

  return (
    <div className="ai-tools-container">
      <div className="ai-tools-header">
        <h2>أدوات الذكاء الاصطناعي</h2>
        <p>مجموعة من الأدوات المدعومة بالذكاء الاصطناعي لمساعدتك في كتابة وتحسين وفهم الكود</p>
      </div>
      
      <div className="ai-tools-filters">
        <button
          className={`filter-button ${activeFilter === 'all' ? 'active' : ''}`}
          onClick={() => handleFilterChange('all')}
        >
          جميع الأدوات
        </button>
        <button
          className={`filter-button ${activeFilter === 'generate_code' ? 'active' : ''}`}
          onClick={() => handleFilterChange('generate_code')}
        >
          توليد الكود
        </button>
        <button
          className={`filter-button ${activeFilter === 'debug_code' ? 'active' : ''}`}
          onClick={() => handleFilterChange('debug_code')}
        >
          تصحيح الأخطاء
        </button>
        <button
          className={`filter-button ${activeFilter === 'explain_code' ? 'active' : ''}`}
          onClick={() => handleFilterChange('explain_code')}
        >
          شرح الكود
        </button>
        <button
          className={`filter-button ${activeFilter === 'convert_code' ? 'active' : ''}`}
          onClick={() => handleFilterChange('convert_code')}
        >
          تحويل الكود
        </button>
      </div>
      
      {loading ? (
        <div className="loading-spinner">جاري تحميل الأدوات...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : filteredTools.length === 0 ? (
        <div className="no-tools-message">
          لا توجد أدوات متاحة في هذه الفئة.
        </div>
      ) : (
        <div className="ai-tools-grid">
          {filteredTools.map((tool) => (
            <AIToolCard key={tool.id} tool={tool} />
          ))}
        </div>
      )}
    </div>
  );
};

export default AIToolList;

