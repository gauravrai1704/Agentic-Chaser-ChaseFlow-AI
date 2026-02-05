const API_BASE = 'http://localhost:8000/api';

export const api = {
  async get(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`);
    if (!response.ok) throw new Error('API Error');
    return response.json();
  },
  async post(endpoint, data) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('API Error');
    return response.json();
  }
};

export const getDashboardStats = () => api.get('/dashboard/stats');
export const getChaseItems = (filters = {}) => api.get('/chase-items?' + new URLSearchParams(filters));
export const getActivities = (limit = 50) => api.get(`/activities?limit=${limit}`);
export const getAgentStatuses = () => api.get('/agents/status');
export const getAnalytics = () => api.get('/analytics/overview');
export const processItem = (id) => api.post(`/chase-items/${id}/process`, {});
