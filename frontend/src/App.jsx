import React, { useState, useEffect } from 'react';
import { Activity, BarChart3, Users, Clock, TrendingUp, Bot } from 'lucide-react';
import Dashboard from './components/Dashboard';
import AgentMonitor from './components/AgentMonitor';
import ChaseTimeline from './components/ChaseTimeline';
import ClientList from './components/ClientList';
import Analytics from './components/Analytics';
import { getDashboardStats, getAgentStatuses } from './utils/api';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    // Refresh data every 30 seconds
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const dashboardStats = await getDashboardStats();
      setStats(dashboardStats);
      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'agents', label: 'Agent Monitor', icon: Bot },
    { id: 'timeline', label: 'Chase Timeline', icon: Clock },
    { id: 'clients', label: 'Clients', icon: Users },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
  ];

  return (
    <div style={{ minHeight: '100vh', background: '#f5f7fa' }}>
      {/* Header */}
      <header style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        padding: '20px 0',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <div className="container" style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center' 
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Activity size={32} />
            <div>
              <h1 style={{ fontSize: '24px', fontWeight: '700', margin: 0 }}>ChaseFlow AI</h1>
              <p style={{ fontSize: '14px', opacity: 0.9, margin: 0 }}>
                Autonomous Agent System for Financial Advisors
              </p>
            </div>
          </div>
          {stats && (
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '28px', fontWeight: '700' }}>
                {stats.time_saved_hours}h
              </div>
              <div style={{ fontSize: '12px', opacity: 0.9 }}>Time Saved</div>
            </div>
          )}
        </div>
      </header>

      {/* Navigation */}
      <div style={{ background: 'white', borderBottom: '1px solid #e5e7eb' }}>
        <div className="container">
          <nav style={{ display: 'flex', gap: '8px' }}>
            {tabs.map(tab => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '16px 24px',
                    border: 'none',
                    background: activeTab === tab.id ? '#f3f4f6' : 'transparent',
                    borderBottom: activeTab === tab.id ? '3px solid #4f46e5' : '3px solid transparent',
                    color: activeTab === tab.id ? '#4f46e5' : '#6b7280',
                    fontWeight: activeTab === tab.id ? '600' : '500',
                    cursor: 'pointer',
                    transition: 'all 0.3s'
                  }}
                >
                  <Icon size={18} />
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="container" style={{ paddingTop: '30px', paddingBottom: '30px' }}>
        {loading ? (
          <div className="loading">
            <Activity size={48} className="spin" />
            <p>Loading ChaseFlow AI...</p>
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && <Dashboard stats={stats} />}
            {activeTab === 'agents' && <AgentMonitor />}
            {activeTab === 'timeline' && <ChaseTimeline />}
            {activeTab === 'clients' && <ClientList />}
            {activeTab === 'analytics' && <Analytics />}
          </>
        )}
      </main>

      {/* Footer */}
      <footer style={{
        background: 'white',
        borderTop: '1px solid #e5e7eb',
        padding: '20px 0',
        marginTop: '40px'
      }}>
        <div className="container" style={{ textAlign: 'center', color: '#6b7280' }}>
          <p>ChaseFlow AI © 2025 | Built for AdvisoryAI Hack-to-Hire Challenge</p>
          <p style={{ fontSize: '14px', marginTop: '8px' }}>
            Autonomous Agent System | Multi-Agent Orchestration | Predictive Intelligence
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
