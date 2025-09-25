import React from 'react';
import { Link } from 'react-router-dom';

const AIToolCard = ({ tool }) => {
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
  
  // تحديد لون نوع الأداة
  const getToolTypeColor = (type) => {
    switch (type) {
      case 'generate_code':
        return 'tool-type-generate';
      case 'debug_code':
        return 'tool-type-debug';
      case 'explain_code':
        return 'tool-type-explain';
      case 'convert_code':
        return 'tool-type-convert';
      default:
        return '';
    }
  };

  return (
    <div className="ai-tool-card">
      <Link to={`/ai-tools/${tool.id}`} className="ai-tool-link">
        <div className="ai-tool-icon">
          <i className={getToolTypeIcon(tool.tool_type)}></i>
        </div>
        
        <div className="ai-tool-content">
          <h3 className="ai-tool-name">{tool.name}</h3>
          
          <div className={`ai-tool-type ${getToolTypeColor(tool.tool_type)}`}>
            {translateToolType(tool.tool_type)}
          </div>
          
          <p className="ai-tool-description">
            {tool.description.length > 100
              ? `${tool.description.substring(0, 100)}...`
              : tool.description}
          </p>
        </div>
        
        <div className="ai-tool-footer">
          <button className="use-tool-button">
            استخدام الأداة <i className="fas fa-arrow-left"></i>
          </button>
        </div>
      </Link>
    </div>
  );
};

export default AIToolCard;

