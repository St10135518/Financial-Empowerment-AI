import { useState, useEffect } from 'react';
import { DashboardLayout } from './Dashboard';
import { api } from '../utils/api';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Search, TrendingUp, Award, Bell, Loader2, Calendar } from 'lucide-react';

function OpportunityScanner() {
  const [scan, setScan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [marketData, setMarketData] = useState(null);

  useEffect(() => {
    fetchScan();
    fetchMarketData();
  }, []);

  const fetchScan = async () => {
    setLoading(true);
    try {
      const response = await api.getLatestOpportunityScan();
      setScan(response.data);
    } catch (error) {
      if (error.response?.status !== 404) {
        toast.error('Failed to load scan');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchMarketData = async () => {
    try {
      const response = await api.getMarketOverview();
      setMarketData(response.data);
    } catch (error) {
      console.error('Failed to fetch market data');
    }
  };

  const runScan = async () => {
    setScanning(true);
    try {
      const response = await api.scanOpportunities();
      setScan(response.data);
      toast.success('Opportunity scan complete!');
    } catch (error) {
      toast.error('Failed to scan opportunities');
    } finally {
      setScanning(false);
    }
  };

  const riskColors = {
    low: 'bg-green-100 text-green-700',
    moderate: 'bg-yellow-100 text-yellow-700',
    high: 'bg-red-100 text-red-700'
  };

  return (
    <DashboardLayout active="/opportunities">
      <div className="p-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 data-testid="opportunities-title" className="text-4xl font-semibold text-stone-900 mb-2">
              Opportunity Scanner
            </h1>
            <p className="text-lg text-stone-600">AI-powered market insights and personalized opportunities</p>
          </div>
          <Button
            data-testid="scan-opportunities-btn"
            onClick={runScan}
            disabled={scanning}
            className="btn-primary"
          >
            {scanning ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Scanning...
              </>
            ) : (
              <>
                <Search className="mr-2 h-5 w-5" />
                Scan Opportunities
              </>
            )}
          </Button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-stone-500">Loading opportunities...</p>
          </div>
        ) : !scan ? (
          <div className="text-center py-12 bg-white rounded-xl">
            <Search className="h-16 w-16 text-stone-300 mx-auto mb-4" />
            <p className="text-stone-600 mb-4">No scan yet. Run your first opportunity scan!</p>
            <Button onClick={runScan} className="btn-primary">
              Scan for Opportunities
            </Button>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Personalized Alerts */}
            <div className="bg-lime-50 border-2 border-lime-200 rounded-xl p-6">
              <div className="flex items-center gap-2 mb-4">
                <Bell className="h-6 w-6 text-lime-700" />
                <h2 className="text-2xl font-semibold text-stone-900">Personalized Alerts</h2>
              </div>
              <div className="space-y-3">
                {scan.personalized_alerts.map((alert, index) => (
                  <div
                    key={index}
                    data-testid={`alert-${index}`}
                    className="flex items-start gap-3 p-4 bg-white rounded-lg border border-lime-300"
                  >
                    <Bell className="h-5 w-5 text-lime-600 flex-shrink-0 mt-0.5" />
                    <p className="text-stone-700">{alert}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Opportunities */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-6">
                <Award className="h-6 w-6 text-emerald-600" />
                <h2 className="text-2xl font-semibold text-stone-900">Opportunities</h2>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {scan.opportunities.map((opp, index) => (
                  <div
                    key={index}
                    data-testid={`opportunity-${index}`}
                    className="border border-stone-200 rounded-lg p-5 hover:border-emerald-500 hover:shadow-md transition-all"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <span className="px-3 py-1 bg-emerald-100 text-emerald-700 text-xs font-medium rounded-full capitalize">
                        {opp.type}
                      </span>
                      {opp.risk_level && (
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${riskColors[opp.risk_level]}`}>
                          {opp.risk_level} risk
                        </span>
                      )}
                    </div>
                    <h3 className="text-lg font-semibold text-stone-900 mb-2">{opp.title}</h3>
                    <p className="text-sm text-stone-600 mb-3">{opp.description}</p>
                    {opp.deadline && (
                      <div className="flex items-center gap-2 text-sm text-stone-500">
                        <Calendar className="h-4 w-4" />
                        <span>Deadline: {opp.deadline}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Market Trends */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-6">
                <TrendingUp className="h-6 w-6 text-emerald-600" />
                <h2 className="text-2xl font-semibold text-stone-900">Market Trends</h2>
              </div>
              <div className="space-y-3">
                {scan.market_trends.map((trend, index) => (
                  <div
                    key={index}
                    data-testid={`trend-${index}`}
                    className="flex items-start gap-3 p-4 bg-emerald-50 rounded-lg border border-emerald-100"
                  >
                    <TrendingUp className="h-5 w-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                    <p className="text-stone-700">{trend}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Market Data */}
            {marketData && marketData.stocks && marketData.stocks.length > 0 && (
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <h2 className="text-2xl font-semibold text-stone-900 mb-6">Live Market Data</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {marketData.stocks.slice(0, 8).map((stock, index) => (
                    <div
                      key={index}
                      className="p-4 border border-stone-200 rounded-lg hover:border-emerald-500 transition-colors"
                    >
                      <p className="text-sm font-medium text-stone-600 mb-1">{stock.symbol}</p>
                      <p className="text-xl font-semibold mono text-stone-900 mb-1">
                        ${stock.price.toFixed(2)}
                      </p>
                      <p className={`text-sm font-medium ${
                        stock.change_percent >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {stock.change_percent >= 0 ? '+' : ''}{stock.change_percent.toFixed(2)}%
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default OpportunityScanner;
