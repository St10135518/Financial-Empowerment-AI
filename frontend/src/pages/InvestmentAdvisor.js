import { useState, useEffect } from 'react';
import { DashboardLayout } from './Dashboard';
import { api } from '../utils/api';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Lightbulb, TrendingUp, Shield, Loader2, PieChart } from 'lucide-react';

function InvestmentAdvisor() {
  const [advice, setAdvice] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchAdvice();
  }, []);

  const fetchAdvice = async () => {
    setLoading(true);
    try {
      const response = await api.getLatestInvestmentAdvice();
      setAdvice(response.data);
    } catch (error) {
      if (error.response?.status !== 404) {
        toast.error('Failed to load advice');
      }
    } finally {
      setLoading(false);
    }
  };

  const getAdvice = async () => {
    setGenerating(true);
    try {
      const response = await api.getInvestmentAdvice();
      setAdvice(response.data);
      toast.success('Investment advice generated!');
    } catch (error) {
      toast.error('Failed to generate advice');
    } finally {
      setGenerating(false);
    }
  };

  const riskColors = {
    none: 'bg-gray-100 text-gray-700',
    low: 'bg-green-100 text-green-700',
    moderate: 'bg-yellow-100 text-yellow-700',
    high: 'bg-red-100 text-red-700'
  };

  return (
    <DashboardLayout active="/investment">
      <div className="p-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 data-testid="investment-title" className="text-4xl font-semibold text-stone-900 mb-2">
              Investment Advisor
            </h1>
            <p className="text-lg text-stone-600">AI-powered personalized investment strategies</p>
          </div>
          <Button
            data-testid="get-advice-btn"
            onClick={getAdvice}
            disabled={generating}
            className="btn-primary"
          >
            {generating ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Lightbulb className="mr-2 h-5 w-5" />
                Get Investment Advice
              </>
            )}
          </Button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-stone-500">Loading advice...</p>
          </div>
        ) : !advice ? (
          <div className="text-center py-12 bg-white rounded-xl">
            <Lightbulb className="h-16 w-16 text-stone-300 mx-auto mb-4" />
            <p className="text-stone-600 mb-4">No investment advice yet. Get personalized guidance!</p>
            <Button onClick={getAdvice} className="btn-primary">
              Get Investment Advice
            </Button>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Risk Assessment Card */}
            <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-6">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-full bg-blue-200 flex items-center justify-center flex-shrink-0">
                  <Shield className="h-6 w-6 text-blue-900" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-stone-900 mb-2">Risk Assessment</h2>
                  <p className="text-stone-700 leading-relaxed">{advice.risk_assessment}</p>
                  <div className="mt-3">
                    <span className="inline-block px-3 py-1 bg-blue-200 text-blue-900 text-sm font-medium rounded-full capitalize">
                      {advice.level} Level
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Investment Recommendations */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-6">
                <PieChart className="h-6 w-6 text-emerald-600" />
                <h2 className="text-2xl font-semibold text-stone-900">Portfolio Recommendations</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {advice.recommendations.map((rec, index) => (
                  <div
                    key={index}
                    data-testid={`investment-recommendation-${index}`}
                    className="border border-stone-200 rounded-lg p-4 hover:border-emerald-500 hover:shadow-md transition-all"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-lg font-semibold text-stone-900">{rec.type}</h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${riskColors[rec.risk]}`}>
                        {rec.risk} risk
                      </span>
                    </div>
                    <div className="mb-3">
                      <p className="text-3xl font-bold text-emerald-600 mono">{rec.allocation}%</p>
                      <p className="text-xs text-stone-500">Allocation</p>
                    </div>
                    <p className="text-sm text-stone-600">{rec.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Portfolio Strategy */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-6">
                <TrendingUp className="h-6 w-6 text-lime-600" />
                <h2 className="text-2xl font-semibold text-stone-900">Portfolio Strategy</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="p-4 bg-lime-50 rounded-lg border border-lime-200">
                  <p className="text-sm text-stone-600 mb-1">Strategy</p>
                  <p className="text-lg font-semibold text-stone-900">
                    {advice.portfolio_suggestion.strategy}
                  </p>
                </div>
                <div className="p-4 bg-lime-50 rounded-lg border border-lime-200">
                  <p className="text-sm text-stone-600 mb-1">Rebalance</p>
                  <p className="text-lg font-semibold text-stone-900 capitalize">
                    {advice.portfolio_suggestion.rebalance_frequency}
                  </p>
                </div>
                <div className="p-4 bg-lime-50 rounded-lg border border-lime-200">
                  <p className="text-sm text-stone-600 mb-1">Expected Return</p>
                  <p className="text-lg font-semibold text-emerald-600">
                    {advice.portfolio_suggestion.expected_return}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default InvestmentAdvisor;
