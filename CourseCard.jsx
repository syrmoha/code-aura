import React from 'react';
import { Link } from 'react-router-dom';

const CourseCard = ({ course }) => {
  // حساب متوسط التقييم
  const averageRating = course.ratings && course.ratings.length > 0
    ? course.ratings.reduce((sum, rating) => sum + rating.rating, 0) / course.ratings.length
    : 0;
  
  // تنسيق متوسط التقييم إلى رقم عشري واحد
  const formattedRating = averageRating.toFixed(1);
  
  // تحويل الدقائق إلى ساعات ودقائق
  const formatDuration = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours} ساعة ${mins > 0 ? `و ${mins} دقيقة` : ''}`;
  };
  
  // تحديد لون المستوى
  const getLevelColor = (level) => {
    switch (level) {
      case 'beginner':
        return 'level-beginner';
      case 'intermediate':
        return 'level-intermediate';
      case 'advanced':
        return 'level-advanced';
      default:
        return '';
    }
  };
  
  // ترجمة المستوى إلى العربية
  const translateLevel = (level) => {
    switch (level) {
      case 'beginner':
        return 'مبتدئ';
      case 'intermediate':
        return 'متوسط';
      case 'advanced':
        return 'متقدم';
      default:
        return level;
    }
  };
  
  // ترجمة اللغة إلى العربية
  const translateLanguage = (language) => {
    switch (language) {
      case 'arabic':
        return 'العربية';
      case 'english':
        return 'الإنجليزية';
      default:
        return language;
    }
  };

  return (
    <div className="course-card">
      <Link to={`/courses/${course.id}`} className="course-card-link">
        <div className="course-card-image">
          {/* استخدام صورة مصغرة من يوتيوب إذا كانت متاحة */}
          <img 
            src={course.thumbnail_url || `https://img.youtube.com/vi/${course.youtube_video_id}/mqdefault.jpg`} 
            alt={course.title} 
          />
          <div className="course-language">{translateLanguage(course.language)}</div>
        </div>
        
        <div className="course-card-content">
          <h3 className="course-title">{course.title}</h3>
          
          <div className="course-meta">
            <div className="course-instructor">
              <i className="fas fa-user"></i> {course.instructor_name}
            </div>
            
            <div className="course-rating">
              <i className="fas fa-star"></i> {formattedRating}
              <span className="rating-count">({course.ratings?.length || 0})</span>
            </div>
          </div>
          
          <div className="course-details">
            <div className={`course-level ${getLevelColor(course.level)}`}>
              <i className="fas fa-signal"></i> {translateLevel(course.level)}
            </div>
            
            <div className="course-duration">
              <i className="fas fa-clock"></i> {formatDuration(course.duration_minutes)}
            </div>
          </div>
          
          <div className="course-programming-language">
            <i className="fas fa-code"></i> {course.programming_language}
          </div>
          
          <p className="course-description">
            {course.description.length > 100
              ? `${course.description.substring(0, 100)}...`
              : course.description}
          </p>
        </div>
      </Link>
    </div>
  );
};

export default CourseCard;

