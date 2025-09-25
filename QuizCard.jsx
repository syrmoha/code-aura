import React from 'react';
import { Link } from 'react-router-dom';

const QuizCard = ({ quiz }) => {
  // ترجمة المستوى إلى العربية
  const translateLevel = (level) => {
    switch (level) {
      case 'easy':
        return 'سهل';
      case 'medium':
        return 'متوسط';
      case 'hard':
        return 'صعب';
      default:
        return level;
    }
  };
  
  // تحديد لون المستوى
  const getLevelColor = (level) => {
    switch (level) {
      case 'easy':
        return 'level-easy';
      case 'medium':
        return 'level-medium';
      case 'hard':
        return 'level-hard';
      default:
        return '';
    }
  };
  
  // تحديد أيقونة لغة البرمجة
  const getProgrammingLanguageIcon = (language) => {
    switch (language) {
      case 'Python':
        return 'fab fa-python';
      case 'JavaScript':
        return 'fab fa-js';
      case 'Java':
        return 'fab fa-java';
      case 'C++':
        return 'fas fa-code';
      case 'SQL':
        return 'fas fa-database';
      default:
        return 'fas fa-code';
    }
  };

  return (
    <div className="quiz-card">
      <Link to={`/quizzes/${quiz.id}`} className="quiz-card-link">
        <div className="quiz-card-header">
          <div className={`quiz-level ${getLevelColor(quiz.level)}`}>
            {translateLevel(quiz.level)}
          </div>
          <div className="quiz-language">
            <i className={getProgrammingLanguageIcon(quiz.programming_language)}></i>
            {quiz.programming_language}
          </div>
        </div>
        
        <div className="quiz-card-content">
          <h3 className="quiz-title">{quiz.title}</h3>
          
          <p className="quiz-description">
            {quiz.description.length > 100
              ? `${quiz.description.substring(0, 100)}...`
              : quiz.description}
          </p>
          
          <div className="quiz-meta">
            <div className="quiz-questions">
              <i className="fas fa-question-circle"></i> {quiz.question_count} سؤال
            </div>
            
            <div className="quiz-time">
              <i className="fas fa-clock"></i> {quiz.time_limit_minutes} دقيقة
            </div>
          </div>
          
          <div className="quiz-attempts">
            <i className="fas fa-users"></i> {quiz.attempts_count || 0} محاولة
          </div>
        </div>
        
        <div className="quiz-card-footer">
          <button className="start-quiz-button">
            ابدأ الاختبار <i className="fas fa-arrow-left"></i>
          </button>
        </div>
      </Link>
    </div>
  );
};

export default QuizCard;

