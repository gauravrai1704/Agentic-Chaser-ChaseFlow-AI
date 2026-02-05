import React, { useEffect, useState } from 'react';
import { TrendingUp, PieChart } from 'lucide-react';
import { getAnalytics } from '../utils/api';

export default function Analytics() {
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const data = await getAnalytics();
      setAnalytics(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (!analytics) return <div>Loading analytics...</div>;

  return (
    <div>
      <div className="card">
        <h2 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <PieChart size={24} />
          Status Distribution
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
          {Object.entries(analytics.status_distribution || {}).map(([status, count]) => (
            <div key={status} style={{
              padding: '20px',
              borderRadius: '8px',
              background: '#f9fafb',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '32px', fontWeight: '700', color: '#4f46e5' }}>{count}</div>
              <div style={{ fontSize: '14px', color: '#6b7280', textTransform: 'uppercase' }}>{status}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h2 style={{ marginBottom: '20px' }}>Category Distribution</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
          {Object.entries(analytics.category_distribution || {}).map(([category, count]) => (
            <div key={category} style={{
              padding: '20px',
              borderRadius: '8px',
              background: '#f0fdf4',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '32px', fontWeight: '700', color: '#10b981' }}>{count}</div>
              <div style={{ fontSize: '14px', color: '#6b7280', textTransform: 'uppercase' }}>{category}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
