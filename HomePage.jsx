import { Helmet } from 'react-helmet-async';
import Navbar from '@/components/Navbar';
import Hero from '@/components/Hero';
import Features from '@/components/Features';
import PopularCourses from '@/components/PopularCourses';
import TestimonialsSection from '@/components/TestimonialsSection';
import CallToAction from '@/components/CallToAction';
import Footer from '@/components/Footer';

const HomePage = () => {
  return (
    <>
      <Helmet>
        <title>Code Aura - منصة تعليم البرمجة</title>
        <meta name="description" content="منصة Code Aura لتعليم البرمجة باللغة العربية. دورات تعليمية، اختبارات تفاعلية، وأدوات ذكاء اصطناعي." />
      </Helmet>
      
      <Navbar />
      
      <main>
        <Hero />
        <Features />
        <PopularCourses />
        <TestimonialsSection />
        <CallToAction />
      </main>
      
      <Footer />
    </>
  );
};

export default HomePage;

