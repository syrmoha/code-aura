import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { MoonIcon, SunIcon, MenuIcon, XIcon } from 'lucide-react';
import logo from '@/assets/logo.svg';

const Navbar = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  // Handle scroll event
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle('dark');
  };

  // Toggle mobile menu
  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsLoggedIn(false);
    // Redirect to home page
    window.location.href = '/';
  };

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-background shadow-md' : 'bg-transparent'}`}>
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <img src={logo} alt="Code Aura" className="logo" />
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="nav-link text-foreground hover:text-primary">الرئيسية</Link>
            <Link to="/courses" className="nav-link text-foreground hover:text-primary">الدورات</Link>
            <Link to="/quizzes" className="nav-link text-foreground hover:text-primary">الاختبارات</Link>
            <Link to="/games" className="nav-link text-foreground hover:text-primary">الألعاب</Link>
            <Link to="/ai-tools" className="nav-link text-foreground hover:text-primary">أدوات الذكاء الاصطناعي</Link>
            <Link to="/articles" className="nav-link text-foreground hover:text-primary">المقالات</Link>
            <Link to="/forum" className="nav-link text-foreground hover:text-primary">المنتدى</Link>
          </div>

          {/* Right side buttons */}
          <div className="hidden md:flex items-center space-x-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleDarkMode}
              className="rounded-full"
            >
              {darkMode ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
            </Button>

            {isLoggedIn ? (
              <div className="flex items-center space-x-4">
                <Link to="/profile">
                  <Button variant="ghost" className="text-foreground hover:text-primary">
                    الملف الشخصي
                  </Button>
                </Link>
                <Button variant="outline" onClick={handleLogout}>
                  تسجيل الخروج
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link to="/login">
                  <Button variant="ghost" className="text-foreground hover:text-primary">
                    تسجيل الدخول
                  </Button>
                </Link>
                <Link to="/register">
                  <Button variant="default">
                    إنشاء حساب
                  </Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleDarkMode}
              className="mr-2 rounded-full"
            >
              {darkMode ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleMenu}
              className="rounded-full"
            >
              {isMenuOpen ? <XIcon className="h-5 w-5" /> : <MenuIcon className="h-5 w-5" />}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="md:hidden bg-background border-t border-border">
          <div className="container mx-auto px-4 py-2">
            <div className="flex flex-col space-y-2">
              <Link to="/" className="py-2 text-foreground hover:text-primary" onClick={() => setIsMenuOpen(false)}>الرئيسية</Link>
              <Link to="/courses" className="py-2 text-foreground hover:text-primary" onClick={() => setIsMenuOpen(false)}>الدورات</Link>
              <Link to="/quizzes" className="py-2 text-foreground hover:text-primary" onClick={() => setIsMenuOpen(false)}>الاختبارات</Link>
              <Link to="/games" className="py-2 text-foreground hover:text-primary" onClick={() => setIsMenuOpen(false)}>الألعاب</Link>
              <Link to="/ai-tools" className="py-2 text-foreground hover:text-primary" onClick={() => setIsMenuOpen(false)}>أدوات الذكاء الاصطناعي</Link>
              <Link to="/articles" className="py-2 text-foreground hover:text-primary" onClick={() => setIsMenuOpen(false)}>المقالات</Link>
              <Link to="/forum" className="py-2 text-foreground hover:text-primary" onClick={() => setIsMenuOpen(false)}>المنتدى</Link>
              
              <div className="pt-2 border-t border-border">
                {isLoggedIn ? (
                  <>
                    <Link to="/profile" className="block py-2 text-foreground hover:text-primary" onClick={() => setIsMenuOpen(false)}>
                      الملف الشخصي
                    </Link>
                    <Button variant="outline" className="w-full mt-2" onClick={() => { handleLogout(); setIsMenuOpen(false); }}>
                      تسجيل الخروج
                    </Button>
                  </>
                ) : (
                  <>
                    <Link to="/login" className="block py-2 text-foreground hover:text-primary" onClick={() => setIsMenuOpen(false)}>
                      تسجيل الدخول
                    </Link>
                    <Link to="/register" onClick={() => setIsMenuOpen(false)}>
                      <Button variant="default" className="w-full mt-2">
                        إنشاء حساب
                      </Button>
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;

