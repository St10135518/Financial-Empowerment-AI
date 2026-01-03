import { useNavigate } from 'react-router-dom';
import { TrendingUp, Target, Lightbulb, Search, GraduationCap, ArrowRight, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';

function LandingPage() {
  const navigate = useNavigate();

  const features = [
    {
      icon: TrendingUp,
      title: "Income Generation",
      description: "AI analyzes your skills and suggests personalized side hustles and freelance opportunities."
    },
    {
      icon: Target,
      title: "Smart Budgeting",
      description: "Find invisible spending leaks and get behavioral insights to maximize your savings."
    },
    {
      icon: Lightbulb,
      title: "Investment Advisor",
      description: "Multi-level guidance from beginner to advanced with portfolio diversification strategies."
    },
    {
      icon: Search,
      title: "Opportunity Scanner",
      description: "Real-time alerts for grants, competitions, and market opportunities tailored to you."
    },
    {
      icon: GraduationCap,
      title: "Financial Education",
      description: "Interactive lessons and gamified challenges to build your wealth-building knowledge."
    },
    {
      icon: Sparkles,
      title: "AI Financial Advisor",
      description: "24/7 personalized guidance from your AI-powered financial growth partner."
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="gradient-hero relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-6 py-24 md:py-32">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div className="text-white space-y-8">
              <h1 data-testid="hero-title" className="text-5xl md:text-7xl font-light tracking-tight leading-none">
                Your Path to
                <span className="block font-semibold mt-2">Financial Freedom</span>
              </h1>
              <p data-testid="hero-description" className="text-base md:text-lg text-white/90 leading-relaxed max-w-xl">
                AI-powered wealth growth system that works for everyone—from zero to millions. 
                Get personalized strategies, real opportunities, and expert guidance at any financial level.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  data-testid="get-started-btn"
                  onClick={() => navigate('/auth')}
                  className="btn-primary text-base"
                >
                  Start Your Journey
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
                <Button
                  data-testid="learn-more-btn"
                  onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}
                  variant="outline"
                  className="bg-white/10 text-white border-white/20 hover:bg-white/20 rounded-full px-8 py-3"
                >
                  Learn More
                </Button>
              </div>
            </div>
            <div className="hidden md:block">
              <img
                src="https://images.unsplash.com/photo-1758611972895-34286de80d4e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwxfHxmaW5hbmNpYWwlMjBncm93dGglMjBzdWNjZXNzfGVufDB8fHx8MTc2NzQxNzM1Nnww&ixlib=rb-4.1.0&q=85"
                alt="Financial Freedom"
                className="rounded-2xl shadow-2xl max-h-[500px] w-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-24 bg-stone-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 data-testid="features-title" className="text-4xl md:text-5xl font-semibold tracking-tight mb-4">
              Everything You Need to <span className="text-gradient">Grow Wealth</span>
            </h2>
            <p className="text-base md:text-lg text-stone-600 max-w-2xl mx-auto">
              Comprehensive tools and insights to transform your financial future
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  data-testid={`feature-card-${index}`}
                  className="group relative overflow-hidden rounded-2xl bg-white p-8 hover:shadow-xl transition-all duration-500 hover-lift"
                >
                  <div className="mb-4">
                    <div className="w-14 h-14 rounded-full bg-lime-100 flex items-center justify-center">
                      <Icon className="h-7 w-7 text-emerald-900" strokeWidth={1.5} />
                    </div>
                  </div>
                  <h3 className="text-2xl font-semibold mb-3 text-stone-900">{feature.title}</h3>
                  <p className="text-stone-600 leading-relaxed">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-emerald-900 text-white">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 data-testid="cta-title" className="text-4xl md:text-5xl font-semibold mb-6">
            Ready to Build Your Financial Future?
          </h2>
          <p className="text-lg text-white/90 mb-8 max-w-2xl mx-auto">
            Join thousands who are already on their path to financial empowerment. 
            Start with our AI advisor today—completely personalized to your situation.
          </p>
          <Button
            data-testid="cta-button"
            onClick={() => navigate('/auth')}
            className="bg-lime-400 text-black hover:bg-lime-300 rounded-full px-8 py-3 text-base font-medium"
          >
            Get Started Free
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-stone-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-stone-400">
            © 2025 Financial Empowerment AI. Democratizing wealth-building knowledge.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;
