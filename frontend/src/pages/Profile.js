import { useState, useEffect } from 'react';
import { DashboardLayout } from './Dashboard';
import { api } from '../utils/api';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { User, Save, Loader2 } from 'lucide-react';

function Profile() {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    monthly_income: 0,
    monthly_expenses: 0,
    savings_goal: 0,
    risk_tolerance: 'moderate',
    skills: '',
    location: '',
    time_availability: '',
    financial_level: 'beginner'
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [userRes, profileRes] = await Promise.all([
        api.getMe(),
        api.getProfile()
      ]);
      setUser(userRes.data);
      setProfile(profileRes.data);
      setFormData({
        monthly_income: profileRes.data.monthly_income || 0,
        monthly_expenses: profileRes.data.monthly_expenses || 0,
        savings_goal: profileRes.data.savings_goal || 0,
        risk_tolerance: profileRes.data.risk_tolerance || 'moderate',
        skills: profileRes.data.skills.join(', ') || '',
        location: profileRes.data.location || '',
        time_availability: profileRes.data.time_availability || '',
        financial_level: profileRes.data.financial_level || 'beginner'
      });
    } catch (error) {
      toast.error('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      const updateData = {
        ...formData,
        monthly_income: parseFloat(formData.monthly_income),
        monthly_expenses: parseFloat(formData.monthly_expenses),
        savings_goal: parseFloat(formData.savings_goal),
        skills: formData.skills.split(',').map(s => s.trim()).filter(s => s)
      };
      
      await api.updateProfile(updateData);
      toast.success('Profile updated successfully!');
      fetchData();
    } catch (error) {
      toast.error('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  return (
    <DashboardLayout active="/profile">
      <div className="p-8">
        <div className="mb-8">
          <h1 data-testid="profile-title" className="text-4xl font-semibold text-stone-900 mb-2">
            Profile & Settings
          </h1>
          <p className="text-lg text-stone-600">Manage your financial profile and preferences</p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-stone-500">Loading profile...</p>
          </div>
        ) : (
          <div className="max-w-3xl">
            {/* User Info */}
            <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center">
                  <User className="h-8 w-8 text-emerald-900" />
                </div>
                <div>
                  <h2 className="text-2xl font-semibold text-stone-900">{user?.full_name}</h2>
                  <p className="text-stone-600">{user?.email}</p>
                </div>
              </div>
            </div>

            {/* Financial Profile Form */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <h2 className="text-2xl font-semibold text-stone-900 mb-6">Financial Profile</h2>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Financial Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <Label htmlFor="monthly_income">Monthly Income ($)</Label>
                    <Input
                      id="monthly_income"
                      data-testid="monthly-income-input"
                      type="number"
                      step="0.01"
                      value={formData.monthly_income}
                      onChange={(e) => setFormData({ ...formData, monthly_income: e.target.value })}
                      className="mt-1"
                    />
                  </div>
                  <div>
                    <Label htmlFor="monthly_expenses">Monthly Expenses ($)</Label>
                    <Input
                      id="monthly_expenses"
                      data-testid="monthly-expenses-input"
                      type="number"
                      step="0.01"
                      value={formData.monthly_expenses}
                      onChange={(e) => setFormData({ ...formData, monthly_expenses: e.target.value })}
                      className="mt-1"
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="savings_goal">Savings Goal ($)</Label>
                  <Input
                    id="savings_goal"
                    data-testid="savings-goal-input"
                    type="number"
                    step="0.01"
                    value={formData.savings_goal}
                    onChange={(e) => setFormData({ ...formData, savings_goal: e.target.value })}
                    className="mt-1"
                  />
                </div>

                {/* Preferences */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <Label htmlFor="risk_tolerance">Risk Tolerance</Label>
                    <Select
                      value={formData.risk_tolerance}
                      onValueChange={(value) => setFormData({ ...formData, risk_tolerance: value })}
                    >
                      <SelectTrigger data-testid="risk-tolerance-select" className="mt-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="low">Low</SelectItem>
                        <SelectItem value="moderate">Moderate</SelectItem>
                        <SelectItem value="high">High</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="financial_level">Financial Level</Label>
                    <Select
                      value={formData.financial_level}
                      onValueChange={(value) => setFormData({ ...formData, financial_level: value })}
                    >
                      <SelectTrigger data-testid="financial-level-select" className="mt-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="beginner">Beginner</SelectItem>
                        <SelectItem value="intermediate">Intermediate</SelectItem>
                        <SelectItem value="advanced">Advanced</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {/* Personal Details */}
                <div>
                  <Label htmlFor="skills">Skills (comma-separated)</Label>
                  <Input
                    id="skills"
                    data-testid="skills-input"
                    type="text"
                    placeholder="e.g., writing, coding, design"
                    value={formData.skills}
                    onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
                    className="mt-1"
                  />
                </div>

                <div>
                  <Label htmlFor="location">Location</Label>
                  <Input
                    id="location"
                    data-testid="location-input"
                    type="text"
                    placeholder="e.g., New York, USA"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    className="mt-1"
                  />
                </div>

                <div>
                  <Label htmlFor="time_availability">Time Availability</Label>
                  <Input
                    id="time_availability"
                    data-testid="time-availability-input"
                    type="text"
                    placeholder="e.g., part-time, weekends"
                    value={formData.time_availability}
                    onChange={(e) => setFormData({ ...formData, time_availability: e.target.value })}
                    className="mt-1"
                  />
                </div>

                <Button
                  data-testid="save-profile-btn"
                  type="submit"
                  disabled={saving}
                  className="btn-primary w-full md:w-auto"
                >
                  {saving ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="mr-2 h-5 w-5" />
                      Save Profile
                    </>
                  )}
                </Button>
              </form>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Profile;
