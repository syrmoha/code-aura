import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { CheckCircle } from 'lucide-react';

const CallToAction = () => {
  const benefits = [
    'دورات برمجية باللغة العربية',
    'شهادات معتمدة بعد إتمام الدورات',
    'محرر أكواد متكامل',
    'اختبارات تفاعلية',
    'منتدى للنقاش والمساعدة',
    'أدوات ذكاء اصطناعي متقدمة'
  ];

  return (
    <section className="py-16 bg-primary text-primary-foreground">
      <div className="container mx-auto px-4">
        <div className="flex flex-col lg:flex-row items-center">
          <div className="lg:w-1/2 mb-8 lg:mb-0">
            <h2 className="text-3xl font-bold mb-4">ابدأ رحلتك في عالم البرمجة الآن</h2>
            <p className="text-lg mb-6 opacity-90">
              انضم إلى آلاف المتعلمين في منصة Code Aura واكتسب المهارات البرمجية التي تحتاجها لبناء مستقبلك المهني.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-8">
              {benefits.map((benefit, index) => (
                <div key={index} className="flex items-center">
                  <CheckCircle className="h-5 w-5 ml-2 text-secondary" />
                  <span>{benefit}</span>
                </div>
              ))}
            </div>
            
            <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
              <Link to="/register">
                <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                  سجل مجاناً
                </Button>
              </Link>
              <Link to="/courses">
                <Button size="lg" variant="outline" className="w-full sm:w-auto border-white/40 hover:bg-white/10">
                  استكشف الدورات
                </Button>
              </Link>
            </div>
          </div>
          
          <div className="lg:w-1/2 lg:pr-8">
            <div className="bg-white/10 backdrop-blur-sm p-8 rounded-lg border border-white/20 relative overflow-hidden">
              <div className="absolute -top-10 -right-10 w-40 h-40 bg-secondary opacity-20 rounded-full blur-2xl"></div>
              <div className="relative z-10">
                <h3 className="text-2xl font-bold mb-6">احصل على تجربة مجانية</h3>
                <form className="space-y-4">
                  <div>
                    <label className="block text-sm mb-1">الاسم الكامل</label>
                    <input
                      type="text"
                      className="w-full px-4 py-2 rounded-md bg-white/20 border border-white/30 text-white placeholder-white/60"
                      placeholder="أدخل اسمك الكامل"
                    />
                  </div>
                  <div>
                    <label className="block text-sm mb-1">البريد الإلكتروني</label>
                    <input
                      type="email"
                      className="w-full px-4 py-2 rounded-md bg-white/20 border border-white/30 text-white placeholder-white/60"
                      placeholder="أدخل بريدك الإلكتروني"
                    />
                  </div>
                  <div>
                    <label className="block text-sm mb-1">مجال الاهتمام</label>
                    <select className="w-full px-4 py-2 rounded-md bg-white/20 border border-white/30 text-white">
                      <option value="">اختر مجال اهتمامك</option>
                      <option value="web">تطوير الويب</option>
                      <option value="mobile">تطوير الموبايل</option>
                      <option value="data">علوم البيانات</option>
                      <option value="ai">الذكاء الاصطناعي</option>
                      <option value="other">مجال آخر</option>
                    </select>
                  </div>
                  <Button type="submit" className="w-full bg-secondary text-secondary-foreground hover:bg-secondary/90">
                    ابدأ الآن
                  </Button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CallToAction;

