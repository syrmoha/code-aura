import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Star, Clock, ChevronLeft, ChevronRight } from 'lucide-react';

// Placeholder data for courses
const coursesData = [
  {
    id: 1,
    title: 'البرمجة بلغة Python للمبتدئين',
    instructor: 'أحمد محمد',
    thumbnail: 'https://img.youtube.com/vi/rfscVS0vtbw/maxresdefault.jpg',
    rating: 4.8,
    reviews: 320,
    duration: '12 ساعة',
    level: 'مبتدئ',
    language: 'العربية',
    category: 'لغات البرمجة'
  },
  {
    id: 2,
    title: 'تطوير واجهات المستخدم باستخدام React',
    instructor: 'سارة أحمد',
    thumbnail: 'https://img.youtube.com/vi/w7ejDZ8SWv8/maxresdefault.jpg',
    rating: 4.9,
    reviews: 450,
    duration: '15 ساعة',
    level: 'متوسط',
    language: 'العربية',
    category: 'تطوير الويب'
  },
  {
    id: 3,
    title: 'تطوير تطبيقات الموبايل باستخدام Flutter',
    instructor: 'محمد علي',
    thumbnail: 'https://img.youtube.com/vi/1ukSR1GRtMU/maxresdefault.jpg',
    rating: 4.7,
    reviews: 280,
    duration: '18 ساعة',
    level: 'متوسط',
    language: 'العربية',
    category: 'تطوير الموبايل'
  },
  {
    id: 4,
    title: 'أساسيات قواعد البيانات SQL',
    instructor: 'فاطمة حسن',
    thumbnail: 'https://img.youtube.com/vi/HXV3zeQKqGY/maxresdefault.jpg',
    rating: 4.6,
    reviews: 210,
    duration: '10 ساعة',
    level: 'مبتدئ',
    language: 'العربية',
    category: 'قواعد البيانات'
  },
  {
    id: 5,
    title: 'تعلم JavaScript من الصفر إلى الاحتراف',
    instructor: 'خالد عمر',
    thumbnail: 'https://img.youtube.com/vi/PkZNo7MFNFg/maxresdefault.jpg',
    rating: 4.9,
    reviews: 520,
    duration: '20 ساعة',
    level: 'مبتدئ إلى متقدم',
    language: 'العربية',
    category: 'لغات البرمجة'
  },
  {
    id: 6,
    title: 'تطوير الويب الكامل - Full Stack Development',
    instructor: 'عمر خالد',
    thumbnail: 'https://img.youtube.com/vi/nu_pCVPKzTk/maxresdefault.jpg',
    rating: 4.8,
    reviews: 380,
    duration: '30 ساعة',
    level: 'متقدم',
    language: 'العربية',
    category: 'تطوير الويب'
  },
  {
    id: 7,
    title: 'مقدمة في الذكاء الاصطناعي وتعلم الآلة',
    instructor: 'ليلى أحمد',
    thumbnail: 'https://img.youtube.com/vi/JcI5Vnw0b2c/maxresdefault.jpg',
    rating: 4.7,
    reviews: 290,
    duration: '16 ساعة',
    level: 'متوسط',
    language: 'العربية',
    category: 'الذكاء الاصطناعي'
  },
  {
    id: 8,
    title: 'تطوير تطبيقات الويب باستخدام Node.js',
    instructor: 'يوسف محمد',
    thumbnail: 'https://img.youtube.com/vi/Oe421EPjeBE/maxresdefault.jpg',
    rating: 4.6,
    reviews: 240,
    duration: '14 ساعة',
    level: 'متوسط',
    language: 'العربية',
    category: 'تطوير الويب'
  }
];

const PopularCourses = () => {
  const [activeCategory, setActiveCategory] = useState('الكل');
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const coursesPerPage = 4;

  const categories = ['الكل', 'لغات البرمجة', 'تطوير الويب', 'تطوير الموبايل', 'قواعد البيانات', 'الذكاء الاصطناعي'];

  useEffect(() => {
    if (activeCategory === 'الكل') {
      setFilteredCourses(coursesData);
    } else {
      setFilteredCourses(coursesData.filter(course => course.category === activeCategory));
    }
    setCurrentPage(0);
  }, [activeCategory]);

  const totalPages = Math.ceil(filteredCourses.length / coursesPerPage);
  const displayedCourses = filteredCourses.slice(
    currentPage * coursesPerPage,
    (currentPage + 1) * coursesPerPage
  );

  const nextPage = () => {
    setCurrentPage((prev) => (prev + 1) % totalPages);
  };

  const prevPage = () => {
    setCurrentPage((prev) => (prev - 1 + totalPages) % totalPages);
  };

  return (
    <section className="py-16 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <h2 className="text-3xl font-bold mb-2">الدورات الأكثر شعبية</h2>
            <p className="text-muted-foreground">استكشف أفضل الدورات التعليمية في مختلف المجالات</p>
          </div>
          <Link to="/courses">
            <Button variant="outline" className="mt-4 md:mt-0">
              عرض جميع الدورات
            </Button>
          </Link>
        </div>

        <div className="flex overflow-x-auto pb-4 mb-6 scrollbar-hide">
          <div className="flex space-x-2 rtl:space-x-reverse">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setActiveCategory(category)}
                className={`px-4 py-2 rounded-full whitespace-nowrap ${
                  activeCategory === category
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-card text-card-foreground hover:bg-muted'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {displayedCourses.map((course) => (
            <div key={course.id} className="course-card card-hover">
              <div className="relative">
                <img src={course.thumbnail} alt={course.title} className="w-full h-48 object-cover" />
                <span className="badge">{course.language}</span>
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4">
                  <div className="flex items-center text-white">
                    <Star className="h-4 w-4 fill-yellow-400 stroke-yellow-400 ml-1" />
                    <span>{course.rating}</span>
                    <span className="mx-1">•</span>
                    <span className="text-sm">({course.reviews})</span>
                  </div>
                </div>
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-1 line-clamp-2">{course.title}</h3>
                <p className="text-muted-foreground text-sm mb-2">{course.instructor}</p>
                <div className="flex items-center text-sm text-muted-foreground mb-3">
                  <Clock className="h-4 w-4 ml-1" />
                  <span>{course.duration}</span>
                  <span className="mx-2">•</span>
                  <span>{course.level}</span>
                </div>
                <Link to={`/courses/${course.id}`}>
                  <Button variant="default" className="w-full">عرض الدورة</Button>
                </Link>
              </div>
            </div>
          ))}
        </div>

        {totalPages > 1 && (
          <div className="flex justify-center mt-8">
            <div className="flex items-center space-x-2 rtl:space-x-reverse">
              <Button
                variant="outline"
                size="icon"
                onClick={prevPage}
                disabled={currentPage === 0}
              >
                <ChevronRight className="h-4 w-4" />
              </Button>
              <span className="text-muted-foreground">
                {currentPage + 1} من {totalPages}
              </span>
              <Button
                variant="outline"
                size="icon"
                onClick={nextPage}
                disabled={currentPage === totalPages - 1}
              >
                <ChevronLeft className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};

export default PopularCourses;

