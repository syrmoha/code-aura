import { Link } from 'react-router-dom';
import { Facebook, Twitter, Instagram, Linkedin, GithubIcon, Mail } from 'lucide-react';
import logo from '@/assets/logo.svg';

const Footer = () => {
  return (
    <footer className="bg-card text-card-foreground pt-12 pb-8">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo and description */}
          <div className="col-span-1 md:col-span-1">
            <Link to="/" className="flex items-center mb-4">
              <img src={logo} alt="Code Aura" className="logo" />
            </Link>
            <p className="text-muted-foreground mb-4">
              منصة Code Aura هي وجهتك الأولى لتعلم البرمجة باللغة العربية. نقدم دورات تعليمية، اختبارات تفاعلية، وأدوات ذكاء اصطناعي لمساعدتك في رحلة التعلم.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                <Facebook size={20} />
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                <Twitter size={20} />
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                <Instagram size={20} />
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                <Linkedin size={20} />
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                <GithubIcon size={20} />
              </a>
            </div>
          </div>

          {/* Quick links */}
          <div className="col-span-1">
            <h3 className="text-lg font-semibold mb-4">روابط سريعة</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-muted-foreground hover:text-primary transition-colors">الرئيسية</Link>
              </li>
              <li>
                <Link to="/courses" className="text-muted-foreground hover:text-primary transition-colors">الدورات</Link>
              </li>
              <li>
                <Link to="/quizzes" className="text-muted-foreground hover:text-primary transition-colors">الاختبارات</Link>
              </li>
              <li>
                <Link to="/games" className="text-muted-foreground hover:text-primary transition-colors">الألعاب</Link>
              </li>
              <li>
                <Link to="/ai-tools" className="text-muted-foreground hover:text-primary transition-colors">أدوات الذكاء الاصطناعي</Link>
              </li>
              <li>
                <Link to="/articles" className="text-muted-foreground hover:text-primary transition-colors">المقالات</Link>
              </li>
              <li>
                <Link to="/forum" className="text-muted-foreground hover:text-primary transition-colors">المنتدى</Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div className="col-span-1">
            <h3 className="text-lg font-semibold mb-4">مصادر</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/about" className="text-muted-foreground hover:text-primary transition-colors">من نحن</Link>
              </li>
              <li>
                <Link to="/faq" className="text-muted-foreground hover:text-primary transition-colors">الأسئلة الشائعة</Link>
              </li>
              <li>
                <Link to="/privacy" className="text-muted-foreground hover:text-primary transition-colors">سياسة الخصوصية</Link>
              </li>
              <li>
                <Link to="/terms" className="text-muted-foreground hover:text-primary transition-colors">شروط الاستخدام</Link>
              </li>
              <li>
                <Link to="/contact" className="text-muted-foreground hover:text-primary transition-colors">اتصل بنا</Link>
              </li>
            </ul>
          </div>

          {/* Newsletter */}
          <div className="col-span-1">
            <h3 className="text-lg font-semibold mb-4">النشرة البريدية</h3>
            <p className="text-muted-foreground mb-4">
              اشترك في نشرتنا البريدية للحصول على آخر الأخبار والتحديثات.
            </p>
            <form className="flex flex-col space-y-2">
              <input
                type="email"
                placeholder="البريد الإلكتروني"
                className="px-4 py-2 rounded-md bg-input text-foreground"
                required
              />
              <button
                type="submit"
                className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
              >
                اشتراك
              </button>
            </form>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-border mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-muted-foreground text-sm">
            &copy; {new Date().getFullYear()} Code Aura. جميع الحقوق محفوظة.
          </p>
          <div className="flex space-x-4 mt-4 md:mt-0">
            <a href="mailto:info@codeaura.com" className="text-muted-foreground hover:text-primary transition-colors flex items-center">
              <Mail size={16} className="ml-1" />
              <span>info@codeaura.com</span>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

