import { 
  BookOpen, 
  Code, 
  Award, 
  Gamepad2, 
  Bot, 
  MessageSquare, 
  Youtube, 
  Languages 
} from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: <BookOpen className="h-6 w-6" />,
      title: 'دورات تعليمية شاملة',
      description: 'دورات برمجية متنوعة باللغة العربية تغطي مختلف لغات البرمجة والتقنيات الحديثة.'
    },
    {
      icon: <Youtube className="h-6 w-6" />,
      title: 'محتوى فيديو عالي الجودة',
      description: 'شروحات فيديو مفصلة من أفضل المدربين العرب والعالميين مع إمكانية المشاهدة داخل المنصة.'
    },
    {
      icon: <Languages className="h-6 w-6" />,
      title: 'دعم اللغة العربية',
      description: 'تركيز على المحتوى العربي مع توفير دورات باللغة الإنجليزية للراغبين في تطوير مهاراتهم اللغوية.'
    },
    {
      icon: <Code className="h-6 w-6" />,
      title: 'محرر أكواد متكامل',
      description: 'محرر أكواد متطور يدعم أكثر من 20 لغة برمجة مع إمكانية تنفيذ الكود مباشرة.'
    },
    {
      icon: <Award className="h-6 w-6" />,
      title: 'اختبارات تفاعلية',
      description: 'اختبارات برمجية متنوعة بمستويات مختلفة لقياس مستواك وتطوير مهاراتك.'
    },
    {
      icon: <Gamepad2 className="h-6 w-6" />,
      title: 'ألعاب تعليمية',
      description: 'ألعاب برمجية تفاعلية تساعدك على تعلم البرمجة بطريقة ممتعة وشيقة.'
    },
    {
      icon: <Bot className="h-6 w-6" />,
      title: 'أدوات ذكاء اصطناعي',
      description: 'أدوات ذكاء اصطناعي متقدمة لمساعدتك في كتابة وتصحيح الكود وحل المشكلات البرمجية.'
    },
    {
      icon: <MessageSquare className="h-6 w-6" />,
      title: 'مجتمع تفاعلي',
      description: 'منتدى نشط للنقاش وتبادل الخبرات مع مبرمجين آخرين ومساعدة بعضكم البعض.'
    }
  ];

  return (
    <section className="py-16 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">ما يميز منصة Code Aura</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            نقدم لك تجربة تعليمية فريدة ومتكاملة لمساعدتك في رحلة تعلم البرمجة من البداية وحتى الاحتراف.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-card p-6 rounded-lg shadow-sm border border-border card-hover">
              <div className="feature-icon">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;

