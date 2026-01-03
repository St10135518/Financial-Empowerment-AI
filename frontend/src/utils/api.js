import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const getAuthHeader = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const api = {
  // Auth
  register: (data) => axios.post(`${API}/auth/register`, data),
  login: (data) => axios.post(`${API}/auth/login`, data),
  getMe: () => axios.get(`${API}/auth/me`, { headers: getAuthHeader() }),
  
  // Profile
  getProfile: () => axios.get(`${API}/profile`, { headers: getAuthHeader() }),
  updateProfile: (data) => axios.put(`${API}/profile`, data, { headers: getAuthHeader() }),
  
  // Income Generation
  generateIncomeOpportunities: () => axios.post(`${API}/income-generation`, {}, { headers: getAuthHeader() }),
  getIncomeOpportunities: () => axios.get(`${API}/income-generation`, { headers: getAuthHeader() }),
  
  // Budget
  analyzeBudget: () => axios.post(`${API}/budget/analyze`, {}, { headers: getAuthHeader() }),
  getLatestBudgetAnalysis: () => axios.get(`${API}/budget/latest`, { headers: getAuthHeader() }),
  
  // Investment
  getInvestmentAdvice: () => axios.post(`${API}/investment/advice`, {}, { headers: getAuthHeader() }),
  getLatestInvestmentAdvice: () => axios.get(`${API}/investment/latest`, { headers: getAuthHeader() }),
  
  // Opportunities
  scanOpportunities: () => axios.post(`${API}/opportunities/scan`, {}, { headers: getAuthHeader() }),
  getLatestOpportunityScan: () => axios.get(`${API}/opportunities/latest`, { headers: getAuthHeader() }),
  
  // Education
  getLessons: (level = 'all') => axios.get(`${API}/education/lessons?level=${level}`),
  completeLesson: (lessonId) => axios.post(`${API}/education/complete/${lessonId}`, {}, { headers: getAuthHeader() }),
  getProgress: () => axios.get(`${API}/education/progress`, { headers: getAuthHeader() }),
  
  // AI Chat
  sendChatMessage: (message, context) => axios.post(`${API}/ai-chat`, { message, context }, { headers: getAuthHeader() }),
  getChatHistory: () => axios.get(`${API}/ai-chat/history`, { headers: getAuthHeader() }),
  
  // Market Data
  getMarketOverview: () => axios.get(`${API}/market/overview`),
  getStockData: (symbol) => axios.get(`${API}/market/stock/${symbol}`),
  
  // Dashboard
  getDashboardStats: () => axios.get(`${API}/dashboard/stats`, { headers: getAuthHeader() }),
};

export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('token', token);
  } else {
    localStorage.removeItem('token');
  }
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};
