import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Search } from 'lucide-react';

const Hero = () => {
  return (
    <div className="hero-section mt-16 mb-12">
      <div className="container mx-auto px-4 py-16">
        <div className="flex flex-col md:flex-row items-center">
          <div className="md:w-1/2 mb-8 md:mb-0">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              تعلم البرمجة بطريقة مبتكرة مع <span className="text-secondary">Code Aura</span>
            </h1>
            <p className="text-lg mb-8 opacity-90">
              منصة تعليمية متكاملة تقدم دورات برمجية باللغة العربية، اختبارات تفاعلية، وأدوات ذكاء اصطناعي لمساعدتك في رحلة تعلم البرمجة.
            </p>
            <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
              <Link to="/courses">
                <Button size="lg" className="w-full sm:w-auto">
                  استكشف الدورات
                </Button>
              </Link>
              <Link to="/register">
                <Button size="lg" variant="outline" className="w-full sm:w-auto bg-white/20 hover:bg-white/30 text-white border-white/40">
                  سجل مجاناً
                </Button>
              </Link>
            </div>
          </div>
          <div className="md:w-1/2 flex justify-center">
            <div className="relative w-full max-w-md">
              <div className="bg-white/10 backdrop-blur-sm p-6 rounded-lg shadow-xl border border-white/20">
                <h3 className="text-xl font-semibold mb-4 text-white">ابحث عن دورة</h3>
                <div className="relative">
                  <input
                    type="text"
                    placeholder="ابحث عن دورة، لغة برمجة، أو موضوع..."
                    className="w-full px-4 py-3 rounded-lg bg-white/20 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white/50"
                  />
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/70" />
                </div>
                <div className="mt-4 flex flex-wrap gap-2">
                  <span className="px-3 py-1 bg-white/20 rounded-full text-sm text-white">JavaScript</span>
                  <span className="px-3 py-1 bg-white/20 rounded-full text-sm text-white">Python</span>
                  <span className="px-3 py-1 bg-white/20 rounded-full text-sm text-white">React</span>
                  <span className="px-3 py-1 bg-white/20 rounded-full text-sm text-white">Flutter</span>
                  <span className="px-3 py-1 bg-white/20 rounded-full text-sm text-white">PHP</span>
                </div>
              </div>
              <div className="absolute -bottom-4 -left-4 w-24 h-24 bg-secondary rounded-full opacity-50 blur-xl z-[-1]"></div>
              <div className="absolute -top-4 -right-4 w-32 h-32 bg-primary rounded-full opacity-50 blur-xl z-[-1]"></div>
            </div>
          </div>
        </div>
        
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <div className="text-3xl font-bold">+1000</div>
            <div className="text-sm opacity-80">دورة تعليمية</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <div className="text-3xl font-bold">+500</div>
            <div className="text-sm opacity-80">اختبار تفاعلي</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <div className="text-3xl font-bold">+50</div>
            <div className="text-sm opacity-80">لعبة برمجية</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <div className="text-3xl font-bold">+10000</div>
            <div className="text-sm opacity-80">متعلم نشط</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;

