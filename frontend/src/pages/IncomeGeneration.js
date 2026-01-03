import { useState, useEffect } from 'react';
import { DashboardLayout } from './Dashboard';
import { api } from '../utils/api';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Briefcase, Clock, DollarSign, TrendingUp, Loader2 } from 'lucide-react';

function IncomeGeneration() {
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchOpportunities();
  }, []);

  const fetchOpportunities = async () => {
    setLoading(true);
    try {
      const response = await api.getIncomeOpportunities();
      setOpportunities(response.data);
    } catch (error) {
      if (error.response?.status !== 404) {
        toast.error('Failed to load opportunities');
      }
    } finally {
      setLoading(false);
    }
  };

  const generateOpportunities = async () => {
    setGenerating(true);
    try {
      const response = await api.generateIncomeOpportunities();
      setOpportunities(response.data);
      toast.success('New income opportunities generated!');
    } catch (error) {
      toast.error('Failed to generate opportunities');
    } finally {
      setGenerating(false);
    }
  };

  const effortColors = {
    low: 'bg-green-100 text-green-700',
    medium: 'bg-yellow-100 text-yellow-700',
    high: 'bg-red-100 text-red-700'
  };

  return (
    <DashboardLayout active="/income">
      <div className="p-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 data-testid="income-title" className="text-4xl font-semibold text-stone-900 mb-2">
              Income Generation
            </h1>
            <p className="text-lg text-stone-600">AI-powered personalized income opportunities</p>
          </div>
          <Button
            data-testid="generate-opportunities-btn"
            onClick={generateOpportunities}
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
                <TrendingUp className="mr-2 h-5 w-5" />
                Generate Opportunities
              </>
            )}
          </Button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-stone-500">Loading opportunities...</p>
          </div>
        ) : opportunities.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-xl">
            <TrendingUp className="h-16 w-16 text-stone-300 mx-auto mb-4" />
            <p className="text-stone-600 mb-4">No opportunities yet. Generate your first batch!</p>
            <Button onClick={generateOpportunities} className="btn-primary">
              Generate Income Opportunities
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {opportunities.map((opp, index) => (
              <div
                key={opp.id}
                data-testid={`opportunity-card-${index}`}
                className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow border border-stone-200"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-lime-100 flex items-center justify-center">
                      <Briefcase className="h-6 w-6 text-emerald-900" />
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-stone-900">{opp.title}</h3>
                      <span className="text-sm text-stone-500 capitalize">{opp.category}</span>
                    </div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${effortColors[opp.effort_level]}`}>
                    {opp.effort_level} effort
                  </span>
                </div>

                <p className="text-stone-600 mb-4">{opp.description}</p>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="flex items-center gap-2">
                    <DollarSign className="h-5 w-5 text-emerald-600" />
                    <div>
                      <p className="text-xs text-stone-500">Estimated Income</p>
                      <p className="text-sm font-medium text-stone-900">{opp.estimated_income}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="h-5 w-5 text-emerald-600" />
                    <div>
                      <p className="text-xs text-stone-500">Time Commitment</p>
                      <p className="text-sm font-medium text-stone-900">{opp.time_commitment}</p>
                    </div>
                  </div>
                </div>

                <div>
                  <p className="text-xs text-stone-500 mb-2">Skills Required:</p>
                  <div className="flex flex-wrap gap-2">
                    {opp.skills_required.map((skill, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 bg-emerald-50 text-emerald-700 text-xs rounded"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default IncomeGeneration;
