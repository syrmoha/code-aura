import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { quizService } from '../../services/api';
import QuizCard from './QuizCard';

const QuizList = ({ limit = 0 }) => {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    programmingLanguage: 'all',
    level: 'all'
  });
  const [pagination, setPagination] = useState({
    page: 1,
    totalPages: 1
  });

  useEffect(() => {
    fetchQuizzes();
  }, [filters, pagination.page]);

  const fetchQuizzes = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params = {
        page: pagination.page,
        limit: limit || 12
      };
      
      if (filters.programmingLanguage !== 'all') {
        params.programming_language = filters.programmingLanguage;
      }
      
      if (filters.level !== 'all') {
        params.level = filters.level;
      }
      
      const response = await quizService.getAllQuizzes(params);
      
      setQuizzes(response.quizzes);
      setPagination({
        page: response.page,
        totalPages: response.totalPages
      });
    } catch (err) {
      console.error('Error fetching quizzes:', err);
      setError('حدث خطأ أثناء تحميل الاختبارات. يرجى المحاولة مرة أخرى.');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({
      ...filters,
      [name]: value
    });
    setPagination({ ...pagination, page: 1 }); // إعادة تعيين الصفحة عند تغيير الفلاتر
  };

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= pagination.totalPages) {
      setPagination({ ...pagination, page: newPage });
    }
  };

  return (
    <div className="quiz-list-container">
      <div className="quiz-filters">
        <div className="filter-group">
          <label htmlFor="programmingLanguage">لغة البرمجة:</label>
          <select
            id="programmingLanguage"
            name="programmingLanguage"
            value={filters.programmingLanguage}
            onChange={handleFilterChange}
          >
            <option value="all">جميع اللغات</option>
            <option value="Python">Python</option>
            <option value="JavaScript">JavaScript</option>
            <option value="Java">Java</option>
            <option value="C++">C++</option>
            <option value="SQL">SQL</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="level">المستوى:</label>
          <select
            id="level"
            name="level"
            value={filters.level}
            onChange={handleFilterChange}
          >
            <option value="all">جميع المستويات</option>
            <option value="easy">سهل</option>
            <option value="medium">متوسط</option>
            <option value="hard">صعب</option>
          </select>
        </div>
      </div>
      
      {loading ? (
        <div className="loading-spinner">جاري تحميل الاختبارات...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : quizzes.length === 0 ? (
        <div className="no-quizzes-message">
          لا توجد اختبارات متاحة بالمعايير المحددة.
        </div>
      ) : (
        <>
          <div className="quizzes-grid">
            {quizzes.map((quiz) => (
              <QuizCard key={quiz.id} quiz={quiz} />
            ))}
          </div>
          
          {!limit && pagination.totalPages > 1 && (
            <div className="pagination">
              <button
                className="pagination-button"
                onClick={() => handlePageChange(pagination.page - 1)}
                disabled={pagination.page === 1}
              >
                السابق
              </button>
              
              <div className="pagination-pages">
                {Array.from({ length: pagination.totalPages }, (_, i) => i + 1).map((page) => (
                  <button
                    key={page}
                    className={`pagination-page ${pagination.page === page ? 'active' : ''}`}
                    onClick={() => handlePageChange(page)}
                  >
                    {page}
                  </button>
                ))}
              </div>
              
              <button
                className="pagination-button"
                onClick={() => handlePageChange(pagination.page + 1)}
                disabled={pagination.page === pagination.totalPages}
              >
                التالي
              </button>
            </div>
          )}
          
          {limit > 0 && quizzes.length >= limit && (
            <div className="view-all-quizzes">
              <Link to="/quizzes" className="view-all-button">
                عرض جميع الاختبارات
              </Link>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default QuizList;

