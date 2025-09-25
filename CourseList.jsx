import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { courseService } from '../../services/api';
import CourseCard from './CourseCard';

const CourseList = ({ categoryId = null, limit = 0, showFilters = true }) => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    language: 'all',
    level: 'all',
    sort: 'newest'
  });
  const [pagination, setPagination] = useState({
    page: 1,
    totalPages: 1
  });

  useEffect(() => {
    fetchCourses();
  }, [categoryId, filters, pagination.page]);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params = {
        page: pagination.page,
        limit: limit || 12,
        sort: filters.sort
      };
      
      if (filters.language !== 'all') {
        params.language = filters.language;
      }
      
      if (filters.level !== 'all') {
        params.level = filters.level;
      }
      
      let response;
      if (categoryId) {
        response = await courseService.getCoursesByCategory(categoryId, params);
      } else {
        response = await courseService.getAllCourses(params);
      }
      
      setCourses(response.courses);
      setPagination({
        page: response.page,
        totalPages: response.totalPages
      });
    } catch (err) {
      console.error('Error fetching courses:', err);
      setError('حدث خطأ أثناء تحميل الدورات. يرجى المحاولة مرة أخرى.');
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
    <div className="course-list-container">
      {showFilters && (
        <div className="course-filters">
          <div className="filter-group">
            <label htmlFor="language">اللغة:</label>
            <select
              id="language"
              name="language"
              value={filters.language}
              onChange={handleFilterChange}
            >
              <option value="all">جميع اللغات</option>
              <option value="arabic">العربية</option>
              <option value="english">الإنجليزية</option>
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
              <option value="beginner">مبتدئ</option>
              <option value="intermediate">متوسط</option>
              <option value="advanced">متقدم</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label htmlFor="sort">الترتيب:</label>
            <select
              id="sort"
              name="sort"
              value={filters.sort}
              onChange={handleFilterChange}
            >
              <option value="newest">الأحدث</option>
              <option value="oldest">الأقدم</option>
              <option value="rating">التقييم</option>
              <option value="popularity">الشعبية</option>
            </select>
          </div>
        </div>
      )}
      
      {loading ? (
        <div className="loading-spinner">جاري تحميل الدورات...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : courses.length === 0 ? (
        <div className="no-courses-message">
          لا توجد دورات متاحة بالمعايير المحددة.
        </div>
      ) : (
        <>
          <div className="courses-grid">
            {courses.map((course) => (
              <CourseCard key={course.id} course={course} />
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
          
          {limit > 0 && courses.length >= limit && (
            <div className="view-all-courses">
              <Link to="/courses" className="view-all-button">
                عرض جميع الدورات
              </Link>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default CourseList;

