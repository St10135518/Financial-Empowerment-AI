import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { Toaster } from '@/components/ui/sonner';
import LandingPage from './pages/LandingPage';
import Auth from './pages/Auth';
import Dashboard from './pages/Dashboard';
import IncomeGeneration from './pages/IncomeGeneration';
import BudgetAnalysis from './pages/BudgetAnalysis';
import InvestmentAdvisor from './pages/InvestmentAdvisor';
import OpportunityScanner from './pages/OpportunityScanner';
import EducationHub from './pages/EducationHub';
import AIChat from './pages/AIChat';
import Profile from './pages/Profile';
import { isAuthenticated } from './utils/api';
import '@/App.css';

function ProtectedRoute({ children }) {
  return isAuthenticated() ? children : <Navigate to="/auth" />;
}

function App() {
  const [isAuth, setIsAuth] = useState(isAuthenticated());

  useEffect(() => {
    setIsAuth(isAuthenticated());
  }, []);

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={isAuth ? <Navigate to="/dashboard" /> : <LandingPage />} />
          <Route path="/auth" element={isAuth ? <Navigate to="/dashboard" /> : <Auth />} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/income" element={<ProtectedRoute><IncomeGeneration /></ProtectedRoute>} />
          <Route path="/budget" element={<ProtectedRoute><BudgetAnalysis /></ProtectedRoute>} />
          <Route path="/investment" element={<ProtectedRoute><InvestmentAdvisor /></ProtectedRoute>} />
          <Route path="/opportunities" element={<ProtectedRoute><OpportunityScanner /></ProtectedRoute>} />
          <Route path="/education" element={<ProtectedRoute><EducationHub /></ProtectedRoute>} />
          <Route path="/ai-chat" element={<ProtectedRoute><AIChat /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </div>
  );
}

export default App;
