import { useState } from 'react';
import { Star, ChevronLeft, ChevronRight, Quote } from 'lucide-react';
import { Button } from '@/components/ui/button';

// Placeholder data for testimonials
const testimonials = [
  {
    id: 1,
    name: 'أحمد محمود',
    role: 'مطور ويب',
    avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
    content: 'منصة Code Aura غيرت حياتي المهنية بالكامل. تعلمت البرمجة من الصفر وأصبحت الآن مطور ويب محترف. الدورات عالية الجودة والشرح ممتاز باللغة العربية.',
    rating: 5
  },
  {
    id: 2,
    name: 'سارة علي',
    role: 'مهندسة برمجيات',
    avatar: 'https://randomuser.me/api/portraits/women/44.jpg',
    content: 'أفضل منصة عربية لتعلم البرمجة. المحتوى منظم بشكل رائع والاختبارات التفاعلية ساعدتني كثيراً في تثبيت المعلومات. أنصح بها بشدة لكل من يريد تعلم البرمجة.',
    rating: 5
  },
  {
    id: 3,
    name: 'محمد خالد',
    role: 'طالب علوم حاسب',
    avatar: 'https://randomuser.me/api/portraits/men/22.jpg',
    content: 'كطالب جامعي، ساعدتني منصة Code Aura في فهم المواد الدراسية بشكل أفضل. الشرح باللغة العربية سهل علي استيعاب المفاهيم المعقدة في البرمجة.',
    rating: 4
  },
  {
    id: 4,
    name: 'نورا أحمد',
    role: 'مطورة تطبيقات موبايل',
    avatar: 'https://randomuser.me/api/portraits/women/29.jpg',
    content: 'تعلمت تطوير تطبيقات الموبايل من خلال دورات Flutter في Code Aura. المنصة توفر محتوى عملي ومشاريع حقيقية ساعدتني في بناء محفظة أعمال قوية.',
    rating: 5
  },
  {
    id: 5,
    name: 'عمر حسن',
    role: 'مدير تقني',
    avatar: 'https://randomuser.me/api/portraits/men/42.jpg',
    content: 'أنا أدير فريقاً تقنياً واشتركت لجميع أعضاء الفريق في Code Aura. لاحظت تحسناً كبيراً في مهاراتهم وإنتاجيتهم. المنصة استثمار رائع للشركات.',
    rating: 5
  },
  {
    id: 6,
    name: 'ليلى محمد',
    role: 'مصممة ويب',
    avatar: 'https://randomuser.me/api/portraits/women/17.jpg',
    content: 'كمصممة، كنت أريد تعلم البرمجة لفهم عملية تطوير الويب بشكل أفضل. دورات Code Aura كانت مثالية لي، خاصة دورات HTML و CSS و JavaScript.',
    rating: 4
  }
];

const TestimonialsSection = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const itemsPerPage = window.innerWidth >= 1024 ? 3 : window.innerWidth >= 768 ? 2 : 1;
  const totalPages = Math.ceil(testimonials.length / itemsPerPage);

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % totalPages);
  };

  const prevSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + totalPages) % totalPages);
  };

  const displayedTestimonials = testimonials.slice(
    currentIndex * itemsPerPage,
    (currentIndex + 1) * itemsPerPage
  );

  const renderStars = (rating) => {
    return Array(5)
      .fill(0)
      .map((_, i) => (
        <Star
          key={i}
          className={`h-4 w-4 ${
            i < rating ? 'fill-yellow-400 stroke-yellow-400' : 'stroke-gray-300'
          }`}
        />
      ));
  };

  return (
    <section className="py-16 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">ماذا يقول المتعلمون عنا</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            آراء حقيقية من متعلمين استفادوا من منصة Code Aura في رحلتهم لتعلم البرمجة
          </p>
        </div>

        <div className="relative">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {displayedTestimonials.map((testimonial) => (
              <div
                key={testimonial.id}
                className="bg-card p-6 rounded-lg shadow-sm border border-border card-hover"
              >
                <Quote className="h-8 w-8 text-primary opacity-20 mb-4" />
                <p className="text-card-foreground mb-6">{testimonial.content}</p>
                <div className="flex items-center">
                  <img
                    src={testimonial.avatar}
                    alt={testimonial.name}
                    className="w-12 h-12 rounded-full ml-4"
                  />
                  <div>
                    <h4 className="font-semibold">{testimonial.name}</h4>
                    <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                    <div className="flex mt-1">{renderStars(testimonial.rating)}</div>
                  </div>
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
                  onClick={prevSlide}
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
                <span className="text-muted-foreground">
                  {currentIndex + 1} من {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={nextSlide}
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;

