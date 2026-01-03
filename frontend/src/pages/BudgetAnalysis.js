import { useState, useEffect } from 'react';
import { DashboardLayout } from './Dashboard';
import { api } from '../utils/api';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { AlertCircle, TrendingDown, Lightbulb, DollarSign, Loader2 } from 'lucide-react';

function BudgetAnalysis() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    fetchAnalysis();
  }, []);

  const fetchAnalysis = async () => {
    setLoading(true);
    try {
      const response = await api.getLatestBudgetAnalysis();
      setAnalysis(response.data);
    } catch (error) {
      if (error.response?.status !== 404) {
        toast.error('Failed to load analysis');
      }
    } finally {
      setLoading(false);
    }
  };

  const runAnalysis = async () => {
    setAnalyzing(true);
    try {
      const response = await api.analyzeBudget();
      setAnalysis(response.data);
      toast.success('Budget analysis complete!');
    } catch (error) {
      toast.error('Failed to analyze budget');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <DashboardLayout active="/budget">
      <div className="p-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 data-testid="budget-title" className="text-4xl font-semibold text-stone-900 mb-2">
              Budget Analysis
            </h1>
            <p className="text-lg text-stone-600">AI-powered spending insights and savings opportunities</p>
          </div>
          <Button
            data-testid="analyze-budget-btn"
            onClick={runAnalysis}
            disabled={analyzing}
            className="btn-primary"
          >
            {analyzing ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <TrendingDown className="mr-2 h-5 w-5" />
                Analyze Budget
              </>
            )}
          </Button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-stone-500">Loading analysis...</p>
          </div>
        ) : !analysis ? (
          <div className="text-center py-12 bg-white rounded-xl">
            <TrendingDown className="h-16 w-16 text-stone-300 mx-auto mb-4" />
            <p className="text-stone-600 mb-4">No budget analysis yet. Run your first analysis!</p>
            <Button onClick={runAnalysis} className="btn-primary">
              Analyze My Budget
            </Button>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Potential Savings Card */}
            <div className="bg-lime-50 border-2 border-lime-200 rounded-xl p-6">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-full bg-lime-200 flex items-center justify-center">
                  <DollarSign className="h-8 w-8 text-emerald-900" />
                </div>
                <div>
                  <p className="text-sm text-stone-600">Potential Monthly Savings</p>
                  <p className="text-4xl font-semibold text-emerald-900 mono">
                    ${analysis.potential_savings}
                  </p>
                  <p className="text-sm text-stone-600 mt-1">
                    That's ${analysis.potential_savings * 12} per year!
                  </p>
                </div>
              </div>
            </div>

            {/* Spending Leaks */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-6">
                <AlertCircle className="h-6 w-6 text-red-600" />
                <h2 className="text-2xl font-semibold text-stone-900">Spending Leaks Identified</h2>
              </div>
              <div className="space-y-4">
                {analysis.spending_leaks.map((leak, index) => (
                  <div
                    key={index}
                    data-testid={`spending-leak-${index}`}
                    className="flex items-start justify-between p-4 bg-red-50 rounded-lg border border-red-100"
                  >
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-stone-900 mb-1">{leak.category}</h3>
                      <p className="text-sm text-stone-600">{leak.description}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-semibold text-red-600 mono">${leak.amount}</p>
                      <p className="text-xs text-stone-500">per month</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendations */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-6">
                <Lightbulb className="h-6 w-6 text-lime-600" />
                <h2 className="text-2xl font-semibold text-stone-900">Actionable Recommendations</h2>
              </div>
              <div className="space-y-3">
                {analysis.recommendations.map((rec, index) => (
                  <div
                    key={index}
                    data-testid={`recommendation-${index}`}
                    className="flex items-start gap-3 p-4 bg-lime-50 rounded-lg border border-lime-200"
                  >
                    <div className="w-6 h-6 rounded-full bg-lime-200 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-sm font-medium text-emerald-900">{index + 1}</span>
                    </div>
                    <p className="text-stone-700 leading-relaxed">{rec}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default BudgetAnalysis;
