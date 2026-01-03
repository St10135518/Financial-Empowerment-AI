import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { api, setAuthToken } from '../utils/api';
import { toast } from 'sonner';
import {
  LayoutDashboard, TrendingUp, Target, Lightbulb,
  Search, GraduationCap, MessageSquare, User, LogOut,
  DollarSign, PiggyBank, TrendingDown, Award
} from 'lucide-react';
import { Button } from '@/components/ui/button';

function DashboardLayout({ children, active }) {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.getMe();
        setUser(response.data);
      } catch (error) {
        toast.error('Session expired');
        setAuthToken(null);
        navigate('/auth');
      }
    };
    fetchUser();
  }, [navigate]);

  const menuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard' },
    { icon: TrendingUp, label: 'Income Generation', path: '/income' },
    { icon: Target, label: 'Budget Analysis', path: '/budget' },
    { icon: Lightbulb, label: 'Investment Advisor', path: '/investment' },
    { icon: Search, label: 'Opportunity Scanner', path: '/opportunities' },
    { icon: GraduationCap, label: 'Education Hub', path: '/education' },
    { icon: MessageSquare, label: 'AI Chat', path: '/ai-chat' },
    { icon: User, label: 'Profile', path: '/profile' },
  ];

  const handleLogout = () => {
    setAuthToken(null);
    toast.success('Logged out successfully');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-stone-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-emerald-900 text-white flex-shrink-0">
        <div className="p-6">
          <div className="flex items-center gap-2 mb-8">
            <TrendingUp className="h-8 w-8 text-lime-400" />
            <span className="text-xl font-semibold">FinanceAI</span>
          </div>

          <nav className="space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  data-testid={`nav-${item.label.toLowerCase().replace(' ', '-')}`}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    active === item.path
                      ? 'bg-lime-400 text-black'
                      : 'text-white/80 hover:bg-white/10'
                  }`}
                >
                  <Icon className="h-5 w-5" strokeWidth={1.5} />
                  <span className="text-sm font-medium">{item.label}</span>
                </Link>
              );
            })}
          </nav>

          <div className="mt-8 pt-6 border-t border-white/20">
            {user && (
              <div className="mb-4 px-4">
                <p className="text-xs text-white/60 mb-1">Signed in as</p>
                <p className="text-sm font-medium truncate">{user.full_name}</p>
              </div>
            )}
            <Button
              data-testid="logout-btn"
              onClick={handleLogout}
              variant="ghost"
              className="w-full justify-start text-white/80 hover:bg-white/10 hover:text-white"
            >
              <LogOut className="h-5 w-5 mr-3" />
              Logout
            </Button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  );
}

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.getDashboardStats();
        setStats(response.data);
      } catch (error) {
        toast.error('Failed to load dashboard');
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const metricCards = stats ? [
    {
      icon: DollarSign,
      label: 'Monthly Income',
      value: `$${stats.monthly_income.toLocaleString()}`,
      color: 'text-emerald-600',
      bg: 'bg-emerald-50'
    },
    {
      icon: TrendingDown,
      label: 'Monthly Expenses',
      value: `$${stats.monthly_expenses.toLocaleString()}`,
      color: 'text-red-600',
      bg: 'bg-red-50'
    },
    {
      icon: PiggyBank,
      label: 'Monthly Savings',
      value: `$${stats.monthly_savings.toLocaleString()}`,
      color: 'text-lime-600',
      bg: 'bg-lime-50'
    },
    {
      icon: Target,
      label: 'Savings Rate',
      value: `${stats.savings_rate}%`,
      color: 'text-blue-600',
      bg: 'bg-blue-50'
    },
    {
      icon: Award,
      label: 'Total Points',
      value: stats.total_points,
      color: 'text-purple-600',
      bg: 'bg-purple-50'
    },
    {
      icon: GraduationCap,
      label: 'Lessons Completed',
      value: stats.completed_lessons,
      color: 'text-orange-600',
      bg: 'bg-orange-50'
    }
  ] : [];

  return (
    <DashboardLayout active="/dashboard">
      <div className="p-8">
        <div className="mb-8">
          <h1 data-testid="dashboard-title" className="text-4xl font-semibold text-stone-900 mb-2">
            Financial Dashboard
          </h1>
          <p className="text-lg text-stone-600">Your personalized wealth-building overview</p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-stone-500">Loading your financial data...</p>
          </div>
        ) : (
          <>
            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {metricCards.map((metric, index) => {
                const Icon = metric.icon;
                return (
                  <div
                    key={index}
                    data-testid={`metric-${metric.label.toLowerCase().replace(' ', '-')}`}
                    className="metric-card"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="text-sm text-stone-600 mb-2">{metric.label}</p>
                        <p className={`text-3xl font-semibold mono ${metric.color}`}>{metric.value}</p>
                      </div>
                      <div className={`w-12 h-12 rounded-full ${metric.bg} flex items-center justify-center`}>
                        <Icon className={`h-6 w-6 ${metric.color}`} />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <h2 className="text-2xl font-semibold text-stone-900 mb-6">Quick Actions</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Link to="/income" data-testid="quick-action-income">
                  <div className="p-4 border border-stone-200 rounded-lg hover:border-emerald-500 hover:shadow-md transition-all cursor-pointer">
                    <TrendingUp className="h-8 w-8 text-emerald-600 mb-2" />
                    <p className="font-medium text-stone-900">Generate Income Ideas</p>
                  </div>
                </Link>
                <Link to="/budget" data-testid="quick-action-budget">
                  <div className="p-4 border border-stone-200 rounded-lg hover:border-emerald-500 hover:shadow-md transition-all cursor-pointer">
                    <Target className="h-8 w-8 text-emerald-600 mb-2" />
                    <p className="font-medium text-stone-900">Analyze Budget</p>
                  </div>
                </Link>
                <Link to="/investment" data-testid="quick-action-investment">
                  <div className="p-4 border border-stone-200 rounded-lg hover:border-emerald-500 hover:shadow-md transition-all cursor-pointer">
                    <Lightbulb className="h-8 w-8 text-emerald-600 mb-2" />
                    <p className="font-medium text-stone-900">Get Investment Advice</p>
                  </div>
                </Link>
                <Link to="/ai-chat" data-testid="quick-action-ai-chat">
                  <div className="p-4 border border-stone-200 rounded-lg hover:border-emerald-500 hover:shadow-md transition-all cursor-pointer">
                    <MessageSquare className="h-8 w-8 text-emerald-600 mb-2" />
                    <p className="font-medium text-stone-900">Chat with AI Advisor</p>
                  </div>
                </Link>
              </div>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Dashboard;
export { DashboardLayout };
